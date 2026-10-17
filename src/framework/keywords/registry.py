"""Registre des mots-cles : un nom (string) -> une fonction qui agit sur un KeywordContext.

Un mot-cle ne contient aucune logique Selenium ni aucun locator : il appelle uniquement
des methodes deja exposees par les pages/composants/flows existants. Ajouter un mot-cle
ne necessite jamais de modifier ce fichier (Open/Closed) : voir ``catalog.py``.
"""
from __future__ import annotations

from collections.abc import Callable

Keyword = Callable[..., None]

_REGISTRY: dict[str, Keyword] = {}


def keyword(name: str) -> Callable[[Keyword], Keyword]:
    def register(fn: Keyword) -> Keyword:
        if name in _REGISTRY:
            raise ValueError(f"Mot-cle '{name}' deja enregistre")
        _REGISTRY[name] = fn
        return fn

    return register


def get_keyword(name: str) -> Keyword:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"Mot-cle inconnu : '{name}'. Disponibles : {sorted(_REGISTRY)}"
        ) from None


def available_keywords() -> list[str]:
    return sorted(_REGISTRY)
