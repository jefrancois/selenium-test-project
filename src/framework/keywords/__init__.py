"""Couche de tests par mots-cles, au-dessus du Page Object Model existant.

Pense pour qu'une interface QA future puisse composer des scenarios (listes de
mots-cles + parametres) sans ecrire de Python ni connaitre les locators. Voir
``catalog.py`` pour le catalogue de mots-cles et ``tests/keyword_suites/`` pour
des exemples.
"""
from __future__ import annotations

from framework.keywords import catalog  # noqa: F401  (enregistre les mots-cles)
from framework.keywords.registry import available_keywords, get_keyword, keyword

__all__ = ["available_keywords", "get_keyword", "keyword"]
