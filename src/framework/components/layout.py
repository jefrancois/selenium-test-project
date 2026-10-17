"""Sections communes a toutes les pages : en-tete, pied de page, barre travailleur."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.components.base_component import BaseComponent


class Header(BaseComponent):
    ROOT = "header"

    _LOGO = (By.CSS_SELECTOR, "a[href='/']")
    def go_to(self, href: str) -> None:
        self.click((By.CSS_SELECTOR, f"a[href='{href}']"))
        self.wait_for_path(href)

    def click_logo(self) -> None:
        self.click(self._LOGO)
        self.wait_for_path("/")

    def shows_login_links(self) -> bool:
        return self.is_present((By.CSS_SELECTOR, "a[href='/login']"))


class LanguageSwitcher(BaseComponent):
    """Bascule FR / EN, situee dans la barre du haut (hors de <header>)."""

    ROOT = "body"

    _BUTTONS = {
        "fr": (By.CSS_SELECTOR, "button[title='Français']"),
        "en": (By.CSS_SELECTOR, "button[title='English']"),
    }

    def switch_to(self, lang: str) -> None:
        self.click(self._BUTTONS[lang])

    def is_active(self, lang: str) -> bool:
        return self.attribute_of(self._BUTTONS[lang], "aria-pressed") == "true"


class Footer(BaseComponent):
    ROOT = "footer"

    def go_to(self, href: str) -> None:
        link = (By.CSS_SELECTOR, f"a[href='{href}']")
        self.scroll_into_view(link)
        self.click(link)
        self.wait_for_path(href)


class WorkerNavBar(BaseComponent):
    """Barre de navigation de l'espace travailleur."""

    ROOT = "nav:has(a[href='/worker/candidatures'])"

    def go_to(self, href: str) -> None:
        self.click((By.CSS_SELECTOR, f"a[href='{href}']"))
        self.wait_for_path(href)

    def labels(self) -> list[str]:
        return self.texts_of((By.CSS_SELECTOR, "a"))
