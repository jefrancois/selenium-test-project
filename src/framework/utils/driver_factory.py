"""Creation des WebDriver (Selenium Manager telecharge les drivers automatiquement).

Pour ajouter un navigateur : ecrire un constructeur et l'enregistrer dans ``_BUILDERS``.
"""
from __future__ import annotations

from collections.abc import Callable

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

_WINDOW = (1920, 1080)


def _chromium(options: webdriver.ChromeOptions | webdriver.EdgeOptions, headless: bool):
    if headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={_WINDOW[0]},{_WINDOW[1]}")
    return options


def _chrome(headless: bool) -> WebDriver:
    return webdriver.Chrome(options=_chromium(webdriver.ChromeOptions(), headless))


def _edge(headless: bool) -> WebDriver:
    return webdriver.Edge(options=_chromium(webdriver.EdgeOptions(), headless))


def _firefox(headless: bool) -> WebDriver:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    options.add_argument(f"--width={_WINDOW[0]}")
    options.add_argument(f"--height={_WINDOW[1]}")
    return webdriver.Firefox(options=options)


_BUILDERS: dict[str, Callable[[bool], WebDriver]] = {
    "chrome": _chrome,
    "firefox": _firefox,
    "edge": _edge,
}


def create_driver(browser: str, headless: bool = True) -> WebDriver:
    try:
        builder = _BUILDERS[browser]
    except KeyError:
        raise ValueError(
            f"Navigateur '{browser}' non supporte. Choix : {tuple(_BUILDERS)}"
        ) from None
    return builder(headless)
