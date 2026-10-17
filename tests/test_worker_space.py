"""Espace travailleur (connecte), lecture seule : un comportement par test."""
from __future__ import annotations

import pytest
from expectations import (
    CURRENT_YEAR,
    DASHBOARD_SECTIONS,
    PLAN_BUTTONS,
    PRICING_MODES,
    PROFILE_TABS,
    RADIUS_OPTIONS,
    USER_MENU_HREFS,
    WORKER_NAV_LABELS,
    WORKER_NAV_LINKS,
    WORKER_PAGES,
    WORKER_TYPES,
)

from framework.pages.page_factory import PageFactory
from framework.pages.public_pages import HomePage
from framework.pages.worker_pages import (
    AnnualStatementPage,
    WorkerBillingPage,
    WorkerDashboardPage,
    WorkerMessagesPage,
    WorkerPayoutsPage,
    WorkerPlanPage,
    WorkerProfilePage,
    WorkerSearchPage,
)

pytestmark = pytest.mark.worker


def _page_id(page_cls: type) -> str:
    return page_cls.__name__


# --- session ----------------------------------------------------------
@pytest.mark.smoke
def test_session_is_authenticated(worker_site: PageFactory) -> None:
    home = worker_site(HomePage).load()

    assert home.user_menu.is_logged_in()


def test_authenticated_header_hides_login_links(worker_site: PageFactory) -> None:
    home = worker_site(HomePage).load()

    assert not home.header.shows_login_links()


# --- chargement des pages ---------------------------------------------
@pytest.mark.parametrize("page_cls", WORKER_PAGES, ids=_page_id)
def test_worker_page_is_served_on_its_path(worker_site: PageFactory, page_cls) -> None:
    page = worker_site(page_cls).load()

    assert page.current_path == page_cls.path


@pytest.mark.parametrize("page_cls", WORKER_PAGES, ids=_page_id)
def test_worker_page_has_heading(worker_site: PageFactory, page_cls) -> None:
    page = worker_site(page_cls).load()

    assert page.heading


# --- tableau de bord --------------------------------------------------
def test_dashboard_greets_the_user(worker_site: PageFactory) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    assert dashboard.heading.startswith("Bonjour")


def test_dashboard_shows_expected_sections(worker_site: PageFactory) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    assert DASHBOARD_SECTIONS <= set(dashboard.section_titles())


# --- barre de navigation et menus --------------------------------------
def test_worker_nav_bar_labels(worker_site: PageFactory) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    assert dashboard.nav.labels() == WORKER_NAV_LABELS


@pytest.mark.parametrize("href", WORKER_NAV_LINKS)
def test_worker_nav_link_navigates(worker_site: PageFactory, href: str) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    dashboard.nav.go_to(href)

    assert dashboard.current_path == href


def test_user_menu_entries(worker_site: PageFactory) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    dashboard.user_menu.open()

    assert dashboard.user_menu.hrefs() == USER_MENU_HREFS


def test_notifications_menu_leads_to_full_list(worker_site: PageFactory) -> None:
    dashboard = worker_site(WorkerDashboardPage).load()

    dashboard.notifications.see_all()

    assert dashboard.current_path == "/worker/notifications"


# --- profil : un bloc par test -----------------------------------------
def test_profile_identity_form_is_visible(worker_site: PageFactory) -> None:
    assert worker_site(WorkerProfilePage).load().identity.is_form_visible()


def test_profile_identity_is_prefilled(worker_site: PageFactory) -> None:
    profile = worker_site(WorkerProfilePage).load()

    assert profile.identity.first_name


def test_profile_radius_is_visible(worker_site: PageFactory) -> None:
    assert worker_site(WorkerProfilePage).load().preferences.is_radius_visible()


def test_profile_worker_types(worker_site: PageFactory) -> None:
    profile = worker_site(WorkerProfilePage).load()

    assert profile.preferences.worker_types() == WORKER_TYPES


def test_profile_pricing_modes(worker_site: PageFactory) -> None:
    profile = worker_site(WorkerProfilePage).load()

    assert profile.preferences.pricing_modes() == PRICING_MODES


def test_profile_tabs(worker_site: PageFactory) -> None:
    profile = worker_site(WorkerProfilePage).load()

    assert set(profile.tabs.available(PROFILE_TABS)) == set(PROFILE_TABS)


def test_profile_links_to_public_profile(worker_site: PageFactory) -> None:
    profile = worker_site(WorkerProfilePage).load()

    assert "/travailleurs/" in profile.public_profile_href()


# --- autres pages -----------------------------------------------------
def test_job_search_radius_options(worker_site: PageFactory) -> None:
    search = worker_site(WorkerSearchPage).load()

    assert search.radius_options() == RADIUS_OPTIONS


def test_job_search_categories_start_with_all(worker_site: PageFactory) -> None:
    search = worker_site(WorkerSearchPage).load()

    assert search.category_options()[0] == "Toutes"


def test_messages_page_has_search_box(worker_site: PageFactory) -> None:
    assert worker_site(WorkerMessagesPage).load().has_search_box()


def test_payouts_page_has_withdrawal_form(worker_site: PageFactory) -> None:
    assert worker_site(WorkerPayoutsPage).load().has_withdrawal_form()


def test_billing_links_to_plans(worker_site: PageFactory) -> None:
    billing = worker_site(WorkerBillingPage).load()

    billing.open_plans()

    assert billing.current_path == WorkerPlanPage.path


def test_plan_page_offers_upgrades(worker_site: PageFactory) -> None:
    plans = worker_site(WorkerPlanPage).load()

    assert plans.upgrade_buttons() == PLAN_BUTTONS


def test_annual_statement_offers_current_year(worker_site: PageFactory) -> None:
    statement = worker_site(AnnualStatementPage).load()

    assert CURRENT_YEAR in statement.years()
