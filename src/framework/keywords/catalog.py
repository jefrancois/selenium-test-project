"""Catalogue des mots-cles disponibles pour les scenarios JSON.

Chaque fonction est une fine couche au-dessus des pages/flows existants : aucun
locator, aucun appel Selenium direct. Pour ajouter un mot-cle, ecrire une fonction
``def mon_mot_cle(ctx: KeywordContext, **params) -> None`` ici et la decorer avec
``@keyword("mon_mot_cle")`` ; aucune autre modification n'est necessaire.
"""
from __future__ import annotations

import pytest

from framework.flows.workflows import AuthFlow
from framework.keywords.context import KeywordContext
from framework.keywords.pages_registry import resolve_page
from framework.keywords.registry import keyword

# --- navigation ---------------------------------------------------------


@keyword("open_page")
def open_page(ctx: KeywordContext, *, page: str) -> None:
    ctx.current = ctx.pages(resolve_page(page)).load()


@keyword("click_header_link")
def click_header_link(ctx: KeywordContext, *, href: str) -> None:
    ctx.page.header.go_to(href)


@keyword("click_footer_link")
def click_footer_link(ctx: KeywordContext, *, href: str) -> None:
    ctx.page.footer.go_to(href)


@keyword("switch_language")
def switch_language(ctx: KeywordContext, *, lang: str) -> None:
    ctx.page.language.switch_to(lang)


# --- authentification -----------------------------------------------------


@keyword("log_in")
def log_in(ctx: KeywordContext, *, email: str, password: str) -> None:
    if not (email and password):
        pytest.skip("Identifiants vides (variable d'environnement non definie)")
    ctx.current = AuthFlow(ctx.pages).log_in(email, password)


@keyword("log_out")
def log_out(ctx: KeywordContext) -> None:
    ctx.current = AuthFlow(ctx.pages).log_out()


# --- assertions -------------------------------------------------------
# Les mots-cles d'assertion sont les seuls a utiliser `assert` : c'est leur role,
# comme pour toute assertion de test (voir code-review passee sur ce point).


@keyword("assert_current_path")
def assert_current_path(ctx: KeywordContext, *, path: str) -> None:
    assert ctx.page.current_path == path, (
        f"chemin attendu '{path}', obtenu '{ctx.page.current_path}'"
    )


@keyword("assert_heading_contains")
def assert_heading_contains(ctx: KeywordContext, *, text: str) -> None:
    assert text in ctx.page.heading, f"'{text}' absent du titre '{ctx.page.heading}'"


@keyword("assert_title_contains")
def assert_title_contains(ctx: KeywordContext, *, text: str) -> None:
    assert text in ctx.page.title, f"'{text}' absent du titre d'onglet '{ctx.page.title}'"


@keyword("assert_language_active")
def assert_language_active(ctx: KeywordContext, *, lang: str) -> None:
    assert ctx.page.language.is_active(lang), f"langue '{lang}' non active"


@keyword("assert_logged_in")
def assert_logged_in(ctx: KeywordContext) -> None:
    assert ctx.page.user_menu.is_logged_in(), "aucune session active"


@keyword("assert_logged_out")
def assert_logged_out(ctx: KeywordContext) -> None:
    assert ctx.page.user_menu.is_signed_out(), "une session est toujours active"
