"""Navigation publique : un comportement par test (atomique)."""
from __future__ import annotations

import pytest
from expectations import FOOTER_LINKS, HEADER_LINKS, PUBLIC_PAGES

from framework.pages.page_factory import PageFactory
from framework.pages.public_pages import FaqPage, HomePage

pytestmark = pytest.mark.navigation


def _page_id(value: object) -> str | None:
    return getattr(value, "__name__", None)


@pytest.mark.smoke
@pytest.mark.parametrize(("page_cls", "_title"), PUBLIC_PAGES, ids=_page_id)
def test_public_page_is_served_on_its_path(public_site: PageFactory, page_cls, _title) -> None:
    page = public_site(page_cls).load()

    assert page.current_path == page_cls.path


@pytest.mark.parametrize(("page_cls", "title_part"), PUBLIC_PAGES, ids=_page_id)
def test_public_page_title(public_site: PageFactory, page_cls, title_part: str) -> None:
    page = public_site(page_cls).load()

    assert title_part in page.title


@pytest.mark.parametrize(("page_cls", "_title"), PUBLIC_PAGES, ids=_page_id)
def test_public_page_has_heading(public_site: PageFactory, page_cls, _title) -> None:
    page = public_site(page_cls).load()

    assert page.heading


@pytest.mark.parametrize("href", HEADER_LINKS)
def test_header_link_navigates(public_site: PageFactory, href: str) -> None:
    home = public_site(HomePage).load()

    home.header.go_to(href)

    assert home.current_path == href


@pytest.mark.parametrize("href", FOOTER_LINKS)
def test_footer_link_navigates(public_site: PageFactory, href: str) -> None:
    home = public_site(HomePage).load()

    home.footer.go_to(href)

    assert home.current_path == href


def test_logo_returns_home(public_site: PageFactory) -> None:
    page = public_site(FaqPage).load()

    page.header.click_logo()

    assert page.current_path == "/"
