"""Configuration centralisee, lue depuis l'environnement (et un fichier .env optionnel)."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    timeout: int
    user_email: str
    user_password: str

    @classmethod
    def from_env(cls) -> Settings:
        return cls(
            base_url=os.getenv("BASE_URL", "https://lpb-web-psi.vercel.app").rstrip("/"),
            browser=os.getenv("BROWSER", "chrome").lower(),
            headless=os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"},
            timeout=int(os.getenv("TIMEOUT", "10")),
            user_email=os.getenv("USER_EMAIL", ""),
            user_password=os.getenv("USER_PASSWORD", ""),
        )
