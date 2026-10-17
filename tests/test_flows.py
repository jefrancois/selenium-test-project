"""Scenarios : enchainements de flux reutilisant les etapes atomiques (aucun locator ici)."""
from __future__ import annotations

import pytest
from expectations import PLAN_BUTTONS, PREVIOUS_YEAR

from framework.flows.workflows import AuthFlow, WorkerFlow
from framework.pages.page_factory import PageFactory
from framework.pages.worker_pages import AnnualStatementPage, WorkerPlanPage, WorkerProfilePage

pytestmark = [pytest.mark.flow, pytest.mark.worker]


def test_worker_reaches_profile_from_user_menu(worker_site: PageFactory) -> None:
    profile = WorkerFlow(worker_site).open_profile_from_user_menu()

    assert profile.current_path == WorkerProfilePage.path
    assert profile.identity.first_name


def test_worker_filters_jobs_by_radius_and_category(worker_site: PageFactory) -> None:
    search = WorkerFlow(worker_site).open_job_search_from_dashboard()
    category = search.category_options()[1]

    search.choose_radius("25 km")
    search.choose_category(category)

    assert (search.selected_radius, search.selected_category) == ("25 km", category)


def test_worker_consults_previous_year_statement(worker_site: PageFactory) -> None:
    statement = WorkerFlow(worker_site).open_annual_statement_from_payouts()
    assert statement.current_path == AnnualStatementPage.path

    statement.choose_year(PREVIOUS_YEAR)

    assert statement.selected_year == PREVIOUS_YEAR


def test_worker_discovers_plans_from_billing(worker_site: PageFactory) -> None:
    plans = WorkerFlow(worker_site).open_plans_from_billing()

    assert plans.current_path == WorkerPlanPage.path
    assert plans.upgrade_buttons() == PLAN_BUTTONS


def test_session_lifecycle(fresh_site: PageFactory, credentials: tuple[str, str]) -> None:
    """Connexion puis deconnexion, sur un navigateur neuf (modifie la session)."""
    auth = AuthFlow(fresh_site)

    home = auth.log_in(*credentials)
    assert home.user_menu.is_logged_in()

    login = auth.log_out()
    assert login.current_path == "/login"
    assert login.user_menu.is_signed_out()
