import logging
from requests import Session
from typing import Optional

from .error import NetworkError, Unauthorized
from .constants import CONFIG_URL, USER_AGENT


class TinyFileManager(Session):
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        config_url: str = CONFIG_URL,
        user_agent: str = USER_AGENT,
    ):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__qualname__)
        self.url = url
        self.username = username
        self.password = password
        self.config_url = config_url
        self.headers["User-Agent"] = user_agent
        self.location: Optional[str] = self.login()

    def login(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> str:
        res = self.get(self.url)
        if not res.ok:
            raise NetworkError(f"Unreachable {self.url}")
        data = {
            "fm_usr": username or self.username,
            "fm_pwd": password or self.password,
        }
        res = self.post(self.url, data=data, allow_redirects=False)
        if res.status_code != 302 or res.url == self.url:
            raise Unauthorized("Login failed. Invalid username or password")
        return res.url
