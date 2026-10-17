"""Flux metier : enchainements d'etapes atomiques, sans aucune assertion.

Chaque methode compose des actions de pages et retourne la page d'arrivee.
Les tests de scenario assemblent ces flux ; les tests atomiques utilisent les pages.
"""
from __future__ import annotations

from framework.pages.page_factory import PageFactory
from framework.pages.public_pages import HomePage, LoginPage
from framework.pages.worker_pages import (
    AnnualStatementPage,
    WorkerBillingPage,
    WorkerDashboardPage,
    WorkerPayoutsPage,
    WorkerPlanPage,
    WorkerProfilePage,
    WorkerSearchPage,
)


class AuthFlow:
    def __init__(self, pages: PageFactory) -> None:
        self._pages = pages

    def log_in(self, email: str, password: str) -> HomePage:
        self._pages(LoginPage).load().log_in(email, password)
        return self._pages(HomePage)

    def log_out(self) -> LoginPage:
        self._pages(WorkerDashboardPage).load().user_menu.log_out()
        return self._pages(LoginPage)


class WorkerFlow:
    def __init__(self, pages: PageFactory) -> None:
        self._pages = pages

    def open_profile_from_user_menu(self) -> WorkerProfilePage:
        self._pages(WorkerDashboardPage).load().user_menu.go_to(WorkerProfilePage.path)
        return self._pages(WorkerProfilePage)

    def open_job_search_from_dashboard(self) -> WorkerSearchPage:
        self._pages(WorkerDashboardPage).load().go_to_job_search()
        return self._pages(WorkerSearchPage)

    def open_annual_statement_from_payouts(self) -> AnnualStatementPage:
        self._pages(WorkerPayoutsPage).load().open_annual_statement()
        return self._pages(AnnualStatementPage)

    def open_plans_from_billing(self) -> WorkerPlanPage:
        self._pages(WorkerBillingPage).load().open_plans()
        return self._pages(WorkerPlanPage)
