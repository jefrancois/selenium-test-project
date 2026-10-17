"""Execute un Case : chaque etape appelle le mot-cle correspondant du registre."""
from __future__ import annotations

from framework.keywords.context import KeywordContext
from framework.keywords.loader import Case
from framework.keywords.registry import get_keyword


class KeywordStepError(RuntimeError):
    """Une etape d'un scenario a echoue ; le message identifie le cas et l'etape."""


def run_case(ctx: KeywordContext, case: Case) -> None:
    for index, step in enumerate(case.steps, start=1):
        fn = get_keyword(step.keyword)
        try:
            fn(ctx, **step.params)
        except Exception as exc:
            raise KeywordStepError(
                f"[{case.source}::{case.id}] etape {index} ({step.keyword}) a echoue : {exc}"
            ) from exc
