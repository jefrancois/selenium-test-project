"""Blocs de la page « Mon profil » : un composant par section."""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from framework.components.base_component import BaseComponent


class ProfileTabs(BaseComponent):
    ROOT = "main"

    _TABS = (By.CSS_SELECTOR, "button")

    def _wait_for_render(self, names: tuple[str, ...]) -> None:
        try:  # les onglets sont rendus apres le chargement des donnees du profil
            self._wait.until(lambda _: any(t in names for t in self.texts_of(self._TABS)))
        except TimeoutException:
            pass

    def available(self, names: tuple[str, ...]) -> list[str]:
        self._wait_for_render(names)
        return [t for t in self.texts_of(self._TABS) if t in names]

    def is_present(self, name: str) -> bool:
        self._wait_for_render((name,))
        return name in self.texts_of(self._TABS)

    def click(self, name: str) -> None:
        self._wait_for_render((name,))
        for button in self.find_all(self._TABS):
            if button.text.strip() == name:
                button.click()
                return
        raise ValueError(f"onglet introuvable : '{name}'")


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


class PasswordSection(BaseComponent):
    """Formulaire de changement de mot de passe (onglet « Parametres du compte »).

    Verifie uniquement la presence du formulaire : jamais de soumission, pour ne
    pas changer le mot de passe du compte utilise par les tests.
    """

    ROOT = "main"

    _CURRENT = (By.CSS_SELECTOR, "#cur")
    _NEW = (By.CSS_SELECTOR, "#nw")
    _CONFIRM = (By.CSS_SELECTOR, "#cf")
    _SUBMIT_BUTTONS = (By.CSS_SELECTOR, "button[type='submit']")

    def is_form_visible(self) -> bool:
        fields_visible = all(
            self.is_visible(loc) for loc in (self._CURRENT, self._NEW, self._CONFIRM)
        )
        return fields_visible and "Changer le mot de passe" in self.texts_of(self._SUBMIT_BUTTONS)


class IdentityVerificationSection(BaseComponent):
    """Onglet « Verification d'identite » : statuts verifies + formulaire de televersement.

    Verifie la presence du formulaire sans jamais le soumettre (televersement de
    documents reel sur un compte de production).
    """

    ROOT = "main"

    _VERIFICATION_ITEMS = (By.CSS_SELECTOR, "ul.space-y-3 > li")
    _BUTTONS = (By.CSS_SELECTOR, "button")

    def _wait_for_render(self) -> None:
        try:  # le contenu de l'onglet est rendu apres le changement d'onglet
            self._wait.until(
                lambda _: "Soumettre pour vérification" in self.texts_of(self._BUTTONS)
            )
        except TimeoutException:
            pass

    def verified_items(self) -> list[str]:
        self._wait_for_render()
        return self.texts_of(self._VERIFICATION_ITEMS)

    def is_verified(self, item: str) -> bool:
        return any(item in text and "Vérifié" in text for text in self.verified_items())

    def is_upload_form_visible(self) -> bool:
        self._wait_for_render()
        return "Soumettre pour vérification" in self.texts_of(self._BUTTONS)
