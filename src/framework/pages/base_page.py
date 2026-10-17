"""Page de base : ajoute a ElementActions la notion d'URL (ouverture d'une page)."""
from __future__ import annotations

import logging

from selenium.webdriver.remote.webdriver import WebDriver

from framework.core.element_actions import ElementActions, Locator

__all__ = ["BasePage", "Locator"]

log = logging.getLogger(__name__)


class BasePage(ElementActions):
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        super().__init__(driver, timeout)
        self.base_url = base_url

    def open(self, path: str = "") -> None:
        url = f"{self.base_url}/{path.lstrip('/')}"
        log.info("Ouverture de %s", url)
        self.driver.get(url)
