"""Actions Selenium (attentes explicites), decoupees en petites interfaces (ISP).

- ``Locating``    : trouver / lire des elements
- ``Interacting`` : agir sur des elements
- ``UrlAware``    : suivre l'URL courante
``ElementActions`` les assemble pour les pages et composants qui ont besoin des trois.
"""
from __future__ import annotations

import logging

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

Locator = tuple[str, str]
log = logging.getLogger(__name__)


class _Context:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self._wait = WebDriverWait(driver, timeout)

    def _resolve(self, locator: Locator) -> Locator:
        """Point d'extension : les composants restreignent le locator a leur racine."""
        return locator


class Locating(_Context):
    def find(self, locator: Locator) -> WebElement:
        return self._wait.until(ec.visibility_of_element_located(self._resolve(locator)))

    def find_all(self, locator: Locator) -> list[WebElement]:
        return self.driver.find_elements(*self._resolve(locator))

    def is_visible(self, locator: Locator) -> bool:
        try:
            self.find(locator)
        except TimeoutException:
            return False
        return True

    def is_present(self, locator: Locator) -> bool:
        return len(self.find_all(locator)) > 0

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def texts_of(self, locator: Locator) -> list[str]:
        return [e.text.strip() for e in self.find_all(locator) if e.text.strip()]

    def attribute_of(self, locator: Locator, name: str) -> str | None:
        return self.find(locator).get_attribute(name)

    def selected_text(self, locator: Locator) -> str:
        return Select(self.find(locator)).first_selected_option.text

    def option_texts(self, locator: Locator) -> list[str]:
        return [o.text for o in Select(self.find(locator)).options]


class Interacting(Locating):
    def click(self, locator: Locator) -> None:
        log.debug("Clic sur %s", locator)
        self._wait.until(ec.element_to_be_clickable(self._resolve(locator))).click()

    def type_text(self, locator: Locator, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def scroll_into_view(self, locator: Locator) -> None:
        element = self.find(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element
        )

    def select_by_text(self, locator: Locator, text: str) -> None:
        Select(self.find(locator)).select_by_visible_text(text)


class UrlAware(_Context):
    @property
    def current_path(self) -> str:
        return self.driver.execute_script("return location.pathname")

    def wait_for_path(self, path: str) -> None:
        self._wait.until(lambda d: d.execute_script("return location.pathname") == path)


class ElementActions(Interacting, UrlAware):
    """Socle complet pour pages et composants."""
