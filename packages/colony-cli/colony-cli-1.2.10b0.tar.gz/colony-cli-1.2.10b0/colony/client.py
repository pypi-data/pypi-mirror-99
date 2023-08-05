import logging
from urllib.parse import urljoin

from requests import Response, Session

from .exceptions import Unauthorized
from .session import ColonySession

logging.getLogger("urllib3").setLevel(logging.WARNING)


class ColonyClient(object):
    """Base class for Colony API access"""

    API_URL = "api/"

    def __init__(
        self,
        colony_host_prefix: str = "https://",
        colony_host: str = "cloudshellcolony.com",
        space: str = None,
        token: str = None,
        account: str = None,
        email: str = None,
        password: str = None,
        session: ColonySession = ColonySession(),
    ):

        if account:
            self.base_url = urljoin(f"{colony_host_prefix}{account}.{colony_host}", self.API_URL)
        else:
            self.base_url = urljoin(f"{colony_host_prefix}{colony_host}", self.API_URL)

        self.session = session
        self.space = space
        self.account = account

        if token:
            self.token = token

        elif all([account, email, password]):
            self.token = ColonyClient.login(account, email, password, self.session, self.base_url)

        self.session.init_bearer_auth(token)

    def __del__(self):
        if self.session:
            try:
                self.session.close()
            except Exception:
                raise
            finally:
                self.session = None

    @staticmethod
    def login(
        account: str,
        email: str,
        password: str,
        session: Session = ColonySession(),
        endpoint: str = "https://cloudshellcolony.com/api",
    ):
        path = urljoin(endpoint, f"accounts/{account}/login")
        payload = {"email": email, "password": password}
        resp = session.post(url=path, json=payload)
        if resp.status_code != 200:
            # TODO(ddovbii): implement exceptions and error handler
            raise Unauthorized("Login Failed")

        return resp.json().get("access_token", "")

    def request(self, endpoint: str, method: str = "GET", params: dict = None, headers: dict = None) -> Response:
        """Gets response as Json"""
        method = method.upper()

        if method not in ("GET", "PUT", "POST", "DELETE"):
            raise ValueError("Method must be in [GET, POST, PUT, DELETE]")

        if headers:
            self.session.headers.update(headers)

        if method in ("POST", "PUT", "DELETE"):
            self.session.headers.update({"Content-Type": "application/json"})

        if params is None:
            params = {}

        url = urljoin(self.base_url, endpoint)

        request_args = {
            "method": method,
            "url": url,
        }
        if method == "GET":
            request_args["params"] = params
        else:
            request_args["json"] = params

        response = self.session.request(**request_args)

        if response.status_code >= 400:
            # TODO(ddovbii): implement exceptions and error handler
            message = ";".join([f"{err['name']}: {err['message']}" for err in response.json().get("errors", [])])
            raise Exception(message)

        return response
