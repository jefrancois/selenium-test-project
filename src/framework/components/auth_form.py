"""Formulaire d'authentification partage par les pages de connexion et d'inscription."""
from __future__ import annotations

from selenium.webdriver.common.by import By

from framework.components.base_component import BaseComponent


class AuthForm(BaseComponent):
    ROOT = "form"

    _EMAIL = (By.CSS_SELECTOR, "#email")
    _PASSWORD = (By.CSS_SELECTOR, "#password")
    _TOGGLE = (By.CSS_SELECTOR, "button[aria-label='Afficher le mot de passe']")
    _SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    def fill_credentials(self, email: str, password: str) -> None:
        self.type_text(self._EMAIL, email)
        self.type_text(self._PASSWORD, password)

    def submit(self) -> None:
        self.click(self._SUBMIT)

    def is_submit_enabled(self) -> bool:
        return self.find(self._SUBMIT).is_enabled()

    def toggle_password_visibility(self) -> None:
        self.click(self._TOGGLE)

    @property
    def password_type(self) -> str:
        return self.attribute_of(self._PASSWORD, "type") or ""
