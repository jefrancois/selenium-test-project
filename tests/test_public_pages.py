"""Contenu et composants des pages publiques : un comportement par test."""
from __future__ import annotations

import pytest

from framework.pages.page_factory import PageFactory
from framework.pages.public_pages import (
    ContactPage,
    FaqPage,
    HomePage,
    LoginPage,
    RegisterPage,
    SearchPage,
    WorkersPage,
)

pytestmark = pytest.mark.navigation


def test_home_lists_categories(public_site: PageFactory) -> None:
    home = public_site(HomePage).load()

    assert home.category_card_count() > 0


def test_faq_has_several_questions(public_site: PageFactory) -> None:
    faq = public_site(FaqPage).load()

    assert faq.question_count() > 1


def test_faq_question_opens(public_site: PageFactory) -> None:
    faq = public_site(FaqPage).load()

    faq.toggle_question(1)

    assert faq.is_question_open(1)


def test_contact_form_is_complete(public_site: PageFactory) -> None:
    assert public_site(ContactPage).load().has_form()


@pytest.mark.parametrize("page_cls", [SearchPage, WorkersPage], ids=lambda c: c.__name__)
def test_search_pages_expose_their_form(public_site: PageFactory, page_cls) -> None:
    assert public_site(page_cls).load().has_search_form()


def test_login_password_is_masked_by_default(public_site: PageFactory) -> None:
    login = public_site(LoginPage).load()

    assert login.form.password_type == "password"


def test_login_password_can_be_revealed(public_site: PageFactory) -> None:
    login = public_site(LoginPage).load()

    login.form.toggle_password_visibility()

    assert login.form.password_type == "text"


def test_register_is_disabled_until_form_is_filled(public_site: PageFactory) -> None:
    register = public_site(RegisterPage).load()

    assert not register.form.is_submit_enabled()


def test_language_can_be_switched_to_english(fresh_site: PageFactory) -> None:
    """Navigateur neuf : la langue choisie est memorisee par le site."""
    home = fresh_site(HomePage).load()

    home.language.switch_to("en")

    assert home.language.is_active("en")
