"""Page du site : compose les sections communes (en-tete, menus, pied de page).

Les composants sont injectables (parametres nommes) et construits par defaut sinon.
"""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.components.layout import Footer, Header, LanguageSwitcher
from framework.components.menus import NotificationsMenu, UserMenu
from framework.pages.base_page import BasePage


class SitePage(BasePage):
    path = "/"
    _HEADING = (By.CSS_SELECTOR, "h1")

    def __init__(
        self,
        driver: WebDriver,
        base_url: str,
        timeout: int = 10,
        *,
        header: Header | None = None,
        footer: Footer | None = None,
        user_menu: UserMenu | None = None,
        notifications: NotificationsMenu | None = None,
        language: LanguageSwitcher | None = None,
    ) -> None:
        super().__init__(driver, base_url, timeout)
        self.header = header or Header(driver, timeout)
        self.footer = footer or Footer(driver, timeout)
        self.user_menu = user_menu or UserMenu(driver, timeout)
        self.notifications = notifications or NotificationsMenu(driver, timeout)
        self.language = language or LanguageSwitcher(driver, timeout)

    def load(self):
        self.open(self.path)
        self.find(self._HEADING)
        return self

    @property
    def title(self) -> str:
        return self.driver.title

    @property
    def heading(self) -> str:
        return self.text_of(self._HEADING)
