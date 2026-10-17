"""Pages publiques (sans connexion) du site On Bricole."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.components.auth_form import AuthForm
from framework.pages.site_page import SitePage


class HomePage(SitePage):
    path = "/"

    _CATEGORY_CARDS = (By.CSS_SELECTOR, "a[href^='/recherche?categorie=']")

    def category_card_count(self) -> int:
        return len(self.find_all(self._CATEGORY_CARDS))


class AboutPage(SitePage):
    path = "/a-propos"


class FaqPage(SitePage):
    path = "/faq"

    _QUESTIONS = (By.CSS_SELECTOR, "main button[aria-expanded]")

    def question_count(self) -> int:
        return len(self.find_all(self._QUESTIONS))

    def toggle_question(self, index: int) -> None:
        self.find_all(self._QUESTIONS)[index].click()

    def is_question_open(self, index: int) -> bool:
        return self.find_all(self._QUESTIONS)[index].get_attribute("aria-expanded") == "true"


class PricingPage(SitePage):
    path = "/tarifs"


class GuidePage(SitePage):
    path = "/guide"


class ContactPage(SitePage):
    path = "/contact"

    _FIELDS = tuple(
        (By.CSS_SELECTOR, f"main form {sel}")
        for sel in ("#name", "#email", "#subject", "#message", "button[type='submit']")
    )

    def has_form(self) -> bool:
        return all(self.is_visible(field) for field in self._FIELDS)


class SearchPage(SitePage):
    """Boulots ouverts."""

    path = "/recherche"

    _KEYWORD = (By.CSS_SELECTOR, "main input[placeholder^='Mot-clé']")

    def has_search_form(self) -> bool:
        return self.is_visible(self._KEYWORD)


class WorkersPage(SitePage):
    path = "/travailleurs"

    _LOCATION = (By.CSS_SELECTOR, "main input[aria-label^='Ville ou code postal']")

    def has_search_form(self) -> bool:
        return self.is_visible(self._LOCATION)


class _AuthPage(SitePage):
    """Pages portant un formulaire email / mot de passe."""

    def __init__(
        self, driver: WebDriver, base_url: str, timeout: int = 10, *,
        form: AuthForm | None = None, **components,
    ) -> None:
        super().__init__(driver, base_url, timeout, **components)
        self.form = form or AuthForm(driver, timeout)


class LoginError(RuntimeError):
    """La page de connexion n'a pas atteint l'etat attendu (pas une assertion de test)."""


class LoginPage(_AuthPage):
    path = "/login"

    def log_in(self, email: str, password: str) -> None:
        """Se connecte et attend que la session soit etablie (avatar visible)."""
        self.form.fill_credentials(email, password)
        self.form.submit()
        if not self.user_menu.is_logged_in():
            raise LoginError("Connexion echouee : le menu utilisateur n'apparait pas")


class RegisterPage(_AuthPage):
    path = "/register"
