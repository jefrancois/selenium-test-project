"""Lecture des scenarios JSON et resolution des `${VARIABLE}` d'environnement.

Format d'un fichier (liste de cas, voir tests/keyword_suites/*.json) :

    [
      {
        "id": "identifiant_unique",
        "description": "Phrase lisible par un QA non technique",
        "steps": [
          {"keyword": "open_page", "page": "HomePage"},
          {"keyword": "assert_heading_contains", "text": "On Bricole"}
        ]
      }
    ]
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

_VAR_PATTERN = re.compile(r"\$\{(\w+)\}")


def _resolve(value: object) -> object:
    if isinstance(value, str):
        return _VAR_PATTERN.sub(lambda m: os.environ.get(m.group(1), ""), value)
    return value


@dataclass(frozen=True)
class Step:
    keyword: str
    params: dict[str, object]


@dataclass(frozen=True)
class Case:
    id: str
    description: str
    source: str
    steps: tuple[Step, ...]


def _parse_file(path: Path) -> list[Case]:
    entries = json.loads(path.read_text(encoding="utf-8"))
    cases = []
    for entry in entries:
        steps = tuple(
            Step(
                keyword=step["keyword"],
                params={k: _resolve(v) for k, v in step.items() if k != "keyword"},
            )
            for step in entry["steps"]
        )
        cases.append(
            Case(
                id=entry["id"],
                description=entry.get("description", ""),
                source=path.name,
                steps=steps,
            )
        )
    return cases


def discover_cases(directory: Path) -> list[Case]:
    """Tous les cas de tous les fichiers *.json d'un dossier, tries par fichier puis id."""
    cases: list[Case] = []
    for path in sorted(directory.glob("*.json")):
        cases.extend(_parse_file(path))
    return cases
