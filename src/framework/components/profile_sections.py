"""Blocs de la page « Mon profil » : un composant par section."""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from framework.components.base_component import BaseComponent


class ProfileTabs(BaseComponent):
    ROOT = "main"

    _TABS = (By.CSS_SELECTOR, "button")

    def available(self, names: tuple[str, ...]) -> list[str]:
        try:  # les onglets sont rendus apres le chargement des donnees du profil
            self._wait.until(lambda _: any(t in names for t in self.texts_of(self._TABS)))
        except TimeoutException:
            pass
        return [t for t in self.texts_of(self._TABS) if t in names]


class IdentitySection(BaseComponent):
    ROOT = "main"

    _FIRST_NAME = (By.CSS_SELECTOR, "#firstName")
    _LAST_NAME = (By.CSS_SELECTOR, "#lastName")
    _PHONE = (By.CSS_SELECTOR, "#phone")
    _BIO = (By.CSS_SELECTOR, "#bio")

    @property
    def first_name(self) -> str:
        return self.attribute_of(self._FIRST_NAME, "value") or ""

    @property
    def last_name(self) -> str:
        return self.attribute_of(self._LAST_NAME, "value") or ""

    def is_form_visible(self) -> bool:
        return all(
            self.is_visible(loc)
            for loc in (self._FIRST_NAME, self._LAST_NAME, self._PHONE, self._BIO)
        )


class PreferencesSection(BaseComponent):
    ROOT = "main"

    _WORKER_TYPE = (By.CSS_SELECTOR, "#workerType")
    _RADIUS = (By.CSS_SELECTOR, "#radius")
    _PRICING = (By.CSS_SELECTOR, "#pricing")

    def worker_types(self) -> list[str]:
        return self.option_texts(self._WORKER_TYPE)

    def pricing_modes(self) -> list[str]:
        return self.option_texts(self._PRICING)

    def is_radius_visible(self) -> bool:
        return self.is_visible(self._RADIUS)
