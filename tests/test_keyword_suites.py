"""Execute les scenarios ecrits en mots-cles (tests/keyword_suites/*.json).

Chaque cas devient un test pytest independant (meme rapport HTML, meme capture
d'ecran automatique en cas d'echec que les tests Python). Cette couche est
destinee a etre generee par une interface QA non technique plus tard ; les
tests Python existants restent la reference pour la couverture fine.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from framework.keywords import catalog  # noqa: F401  (enregistre les mots-cles)
from framework.keywords.context import KeywordContext
from framework.keywords.loader import Case, discover_cases
from framework.keywords.runner import run_case
from framework.pages.page_factory import PageFactory

pytestmark = pytest.mark.keyword

SUITES_DIR = Path(__file__).resolve().parent / "keyword_suites"
CASES = discover_cases(SUITES_DIR)


def _case_id(case: Case) -> str:
    return f"{case.source}::{case.id}"


@pytest.mark.parametrize("case", CASES, ids=_case_id)
def test_keyword_case(fresh_site: PageFactory, case: Case) -> None:
    run_case(KeywordContext(pages=fresh_site), case)
