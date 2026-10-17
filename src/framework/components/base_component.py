"""Composant : une section de l'interface, cherchee uniquement a l'interieur de sa racine."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.core.element_actions import ElementActions, Locator


class BaseComponent(ElementActions):
    ROOT: str = "body"

    def _resolve(self, locator: Locator) -> Locator:
        by, value = locator
        if by != By.CSS_SELECTOR:
            raise ValueError("Les composants n'utilisent que des locators CSS")
        return (By.CSS_SELECTOR, f"{self.ROOT} {value}")
