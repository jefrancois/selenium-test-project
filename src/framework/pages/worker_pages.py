"""Pages de l'espace travailleur (apres connexion)."""
from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from framework.components.layout import WorkerNavBar
from framework.components.profile_sections import (
    IdentitySection,
    IdentityVerificationSection,
    PasswordSection,
    PreferencesSection,
    ProfileTabs,
)
from framework.pages.site_page import SitePage


class WorkerPage(SitePage):
    """Base de l'espace travailleur : ajoute la barre de navigation interne."""

    _HEADING = (By.CSS_SELECTOR, "main h1, main h2")
    _SECTION_TITLES = (By.CSS_SELECTOR, "main h2")

    def __init__(
        self, driver: WebDriver, base_url: str, timeout: int = 10, *,
        nav: WorkerNavBar | None = None, **components,
    ) -> None:
        super().__init__(driver, base_url, timeout, **components)
        self.nav = nav or WorkerNavBar(driver, timeout)

    def section_titles(self) -> list[str]:
        return self.texts_of(self._SECTION_TITLES)


class WorkerDashboardPage(WorkerPage):
    path = "/worker"

    _HEADING = (By.CSS_SELECTOR, "main h1")
    _JOB_SEARCH = (By.CSS_SELECTOR, "main a[href='/worker/search']")

    def go_to_job_search(self) -> None:
        self.click(self._JOB_SEARCH)
        self.wait_for_path("/worker/search")


class WorkerSearchPage(WorkerPage):
    """Demandes a proximite."""

    path = "/worker/search"

    _CATEGORY = (By.CSS_SELECTOR, "#cat")
    _RADIUS = (By.CSS_SELECTOR, "#radius")

    def radius_options(self) -> list[str]:
        return self.option_texts(self._RADIUS)

    def category_options(self) -> list[str]:
        # les categories sont chargees apres l'affichage de la page
        self._wait.until(lambda _: len(self.option_texts(self._CATEGORY)) > 1)
        return self.option_texts(self._CATEGORY)

    def choose_radius(self, label: str) -> None:
        self.select_by_text(self._RADIUS, label)

    @property
    def selected_radius(self) -> str:
        return self.selected_text(self._RADIUS)

    def choose_category(self, label: str) -> None:
        self.select_by_text(self._CATEGORY, label)

    @property
    def selected_category(self) -> str:
        return self.selected_text(self._CATEGORY)


class WorkerMessagesPage(WorkerPage):
    path = "/worker/messages"

    _SEARCH = (By.CSS_SELECTOR, "main input[placeholder^='Rechercher une conversation']")

    def has_search_box(self) -> bool:
        return self.is_visible(self._SEARCH)


class WorkerProfilePage(WorkerPage):
    path = "/worker/profil"

    _PUBLIC_PROFILE = (By.CSS_SELECTOR, "main a[href^='/travailleurs/']")

    def __init__(
        self, driver: WebDriver, base_url: str, timeout: int = 10, *,
        tabs: ProfileTabs | None = None,
        identity: IdentitySection | None = None,
        preferences: PreferencesSection | None = None,
        password: PasswordSection | None = None,
        identity_verification: IdentityVerificationSection | None = None,
        **components,
    ) -> None:
        super().__init__(driver, base_url, timeout, **components)
        self.tabs = tabs or ProfileTabs(driver, timeout)
        self.identity = identity or IdentitySection(driver, timeout)
        self.preferences = preferences or PreferencesSection(driver, timeout)
        self.password = password or PasswordSection(driver, timeout)
        self.identity_verification = identity_verification or IdentityVerificationSection(
            driver, timeout
        )

    def public_profile_href(self) -> str:
        return self.attribute_of(self._PUBLIC_PROFILE, "href") or ""


class WorkerPayoutsPage(WorkerPage):
    path = "/worker/payouts"

    _AMOUNT = (By.CSS_SELECTOR, "main input[type='number']")
    _WITHDRAW = (By.CSS_SELECTOR, "main button[type='submit']")
    _STATEMENT_LINK = (By.CSS_SELECTOR, "main a[href='/worker/releve']")

    def has_withdrawal_form(self) -> bool:
        return self.is_visible(self._AMOUNT) and self.is_present(self._WITHDRAW)

    def open_annual_statement(self) -> None:
        self.click(self._STATEMENT_LINK)
        self.wait_for_path("/worker/releve")


class WorkerBillingPage(WorkerPage):
    path = "/worker/facturation"

    _PLAN_LINK = (By.CSS_SELECTOR, "main a[href='/worker/forfait']")

    def open_plans(self) -> None:
        self.click(self._PLAN_LINK)
        self.wait_for_path("/worker/forfait")


class WorkerPlanPage(WorkerPage):
    path = "/worker/forfait"

    def upgrade_buttons(self) -> list[str]:
        return self.texts_of((By.CSS_SELECTOR, "main button"))


class WorkerRequestsPage(WorkerPage):
    """Demandes publiees par le travailleur (« Mes demandes »)."""

    path = "/worker/demandes"

    _ACTION_BUTTONS = (By.CSS_SELECTOR, "main button")
    _WIZARD_HEADINGS = (By.CSS_SELECTOR, "main h1")

    def open_new_request_wizard(self) -> None:
        """Ouvre l'etape 1 du formulaire (choix du service), sans jamais publier."""
        for button in self.find_all(self._ACTION_BUTTONS):
            if button.text.strip() == "Nouvelle demande":
                button.click()
                return
        raise ValueError("Bouton 'Nouvelle demande' introuvable")

    def is_service_step_visible(self) -> bool:
        return "Quel service vous faut-il ?" in self.texts_of(self._WIZARD_HEADINGS)


class WorkerNotificationsPage(WorkerPage):
    path = "/worker/notifications"


class AnnualStatementPage(WorkerPage):
    path = "/worker/releve"

    _YEAR = (By.CSS_SELECTOR, "#year")

    def years(self) -> list[str]:
        return self.option_texts(self._YEAR)

    def choose_year(self, year: str) -> None:
        self.select_by_text(self._YEAR, year)

    @property
    def selected_year(self) -> str:
        return self.selected_text(self._YEAR)
