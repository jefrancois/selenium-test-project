"""Fixtures partagees : configuration, drivers, fabriques de pages, rapport et captures.

Trois niveaux d'isolation :
- ``public_site`` / ``worker_site`` : navigateur partage pour toute la session, reserve aux
  tests en lecture seule (chaque test recharge sa page par URL) ;
- ``fresh_site`` : navigateur neuf par test, pour tout test qui modifie l'etat de la session.
"""
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from framework.config import Settings
from framework.flows.workflows import AuthFlow
from framework.pages.page_factory import PageFactory
from framework.utils.driver_factory import create_driver

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser", help="chrome | firefox | edge (ecrase BROWSER)")
    parser.addoption("--headed", action="store_true", help="Navigateur avec interface")


def pytest_html_report_title(report) -> None:
    report.title = "On Bricole - Rapport de tests UI"


def pytest_configure(config: pytest.Config) -> None:
    from pytest_metadata.plugin import metadata_key

    settings = Settings.from_env()
    meta = config.stash[metadata_key]
    meta["URL testee"] = settings.base_url
    meta["Navigateur"] = config.getoption("--browser") or settings.browser


# --- configuration ----------------------------------------------------
@pytest.fixture(scope="session")
def settings(request: pytest.FixtureRequest) -> Settings:
    base = Settings.from_env()
    browser = request.config.getoption("--browser") or base.browser
    headless = False if request.config.getoption("--headed") else base.headless
    return replace(base, browser=browser, headless=headless)


@pytest.fixture(scope="session")
def credentials(settings: Settings) -> tuple[str, str]:
    if not (settings.user_email and settings.user_password):
        pytest.skip("USER_EMAIL / USER_PASSWORD non definis (.env)")
    return settings.user_email, settings.user_password


# --- navigateurs ------------------------------------------------------
@pytest.fixture
def driver(settings: Settings) -> Iterator[WebDriver]:
    drv = create_driver(settings.browser, settings.headless)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def _public_driver(settings: Settings) -> Iterator[WebDriver]:
    drv = create_driver(settings.browser, settings.headless)
    yield drv
    drv.quit()


@pytest.fixture(scope="session")
def _worker_driver(settings: Settings, credentials: tuple[str, str]) -> Iterator[WebDriver]:
    """Une seule connexion pour toute la session (evite de saturer le site)."""
    drv = create_driver(settings.browser, settings.headless)
    try:
        AuthFlow(PageFactory(drv, settings.base_url, settings.timeout)).log_in(*credentials)
        yield drv
    finally:
        drv.quit()


# --- fabriques de pages ----------------------------------------------
@pytest.fixture
def public_site(_public_driver: WebDriver, settings: Settings) -> PageFactory:
    return PageFactory(_public_driver, settings.base_url, settings.timeout)


@pytest.fixture
def worker_site(_worker_driver: WebDriver, settings: Settings) -> PageFactory:
    return PageFactory(_worker_driver, settings.base_url, settings.timeout)


@pytest.fixture
def fresh_site(driver: WebDriver, settings: Settings) -> PageFactory:
    return PageFactory(driver, settings.base_url, settings.timeout)


# --- rapport ----------------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    drv = next(
        (
            v.driver if isinstance(v, PageFactory) else v
            for v in getattr(item, "funcargs", {}).values()
            if isinstance(v, WebDriver | PageFactory)
        ),
        None,
    )
    if drv is None:
        return
    REPORTS_DIR.mkdir(exist_ok=True)
    drv.save_screenshot(str(REPORTS_DIR / f"{item.name}.png"))
    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.image(drv.get_screenshot_as_base64()))
        extras.append(pytest_html.extras.url(drv.current_url, name="URL au moment de l'echec"))
        report.extras = extras
