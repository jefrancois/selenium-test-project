"""Etat porte entre deux mots-cles d'un meme scenario : la fabrique de pages et la
page courante (celle sur laquelle portent les prochaines actions/assertions)."""
from __future__ import annotations

from dataclasses import dataclass

from framework.pages.base_page import BasePage
from framework.pages.page_factory import PageFactory


@dataclass
class KeywordContext:
    pages: PageFactory
    current: BasePage | None = None

    @property
    def page(self) -> BasePage:
        if self.current is None:
            raise RuntimeError(
                "Aucune page ouverte : le premier mot-cle d'un scenario doit etre "
                "'open_page' ou 'log_in'."
            )
        return self.current
