"""Menus deroulants de l'en-tete (visibles uniquement une fois connecte)."""
from __future__ import annotations

import re

from selenium.webdriver.common.by import By

from framework.components.base_component import BaseComponent


class UserMenu(BaseComponent):
    """Avatar + menu : Mon espace, profil, paiements, facturation, deconnexion."""

    ROOT = "body"

    _TRIGGER = (By.CSS_SELECTOR, "header button[aria-haspopup='menu']:not([aria-label])")
    _ITEMS = (By.CSS_SELECTOR, "[role='menu'] a")
    _LOGOUT = (By.CSS_SELECTOR, "[role='menu'] button")

    def is_logged_in(self) -> bool:
        return self.is_visible(self._TRIGGER)

    def is_signed_out(self) -> bool:
        return not self.is_present(self._TRIGGER)

    def open(self) -> None:
        if self.attribute_of(self._TRIGGER, "aria-expanded") != "true":
            self.click(self._TRIGGER)
        self.find(self._ITEMS)

    def hrefs(self) -> list[str]:
        """Attributs href bruts (non resolus) : getAttribute, pas la propriete .href."""
        _, selector = self._resolve(self._ITEMS)
        paths = self.driver.execute_script(
            "return [...document.querySelectorAll(arguments[0])].map(a => a.getAttribute('href'))",
            selector,
        )
        return list(paths)

    def go_to(self, href: str) -> None:
        self.open()
        self.click((By.CSS_SELECTOR, f"[role='menu'] a[href='{href}']"))
        self.wait_for_path(href)

    def log_out(self) -> None:
        self.open()
        self.click(self._LOGOUT)
        self.wait_for_path("/login")


class NotificationsMenu(BaseComponent):
    ROOT = "body"

    _TRIGGER = (By.CSS_SELECTOR, "header button[aria-label^='Notifications']")
    _SEE_ALL = (By.CSS_SELECTOR, "[role='menu'] a[href='/worker/notifications']")

    @property
    def unread_count(self) -> int:
        match = re.search(r"\((\d+)", self.attribute_of(self._TRIGGER, "aria-label") or "")
        return int(match.group(1)) if match else 0

    def open(self) -> None:
        if self.attribute_of(self._TRIGGER, "aria-expanded") != "true":
            self.click(self._TRIGGER)
        self.find(self._SEE_ALL)

    def see_all(self) -> None:
        self.open()
        self.click(self._SEE_ALL)
        self.wait_for_path("/worker/notifications")
