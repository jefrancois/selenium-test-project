"""Fabrique de pages : un seul endroit connait (driver, base_url, timeout)."""
from __future__ import annotations

from typing import TypeVar

from selenium.webdriver.remote.webdriver import WebDriver

from framework.pages.base_page import BasePage

P = TypeVar("P", bound=BasePage)


class PageFactory:
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self.driver = driver
        self._base_url = base_url
        self._timeout = timeout

    def __call__(self, page_cls: type[P]) -> P:
        return page_cls(self.driver, self._base_url, self._timeout)
