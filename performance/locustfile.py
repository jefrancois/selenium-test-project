"""Scenario de charge sur les pages PUBLIQUES de On Bricole (sans connexion).

Ce fichier ne fait que des GET anonymes. Il ne doit jamais etre lance avec un
nombre d'utilisateurs eleve ou un ramp-up instantane contre un site qu'on ne
controle pas pleinement : voir performance/README.md avant de choisir -u/-r.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()

# Garde une barriere de securite dans le code lui-meme : un -u trop eleve
# est refuse plutot que d'etre envoye au serveur. Augmenter ce nombre est un
# choix delibere, pas un defaut.
MAX_SAFE_USERS = 800
if int(os.getenv("LOCUST_USERS", "1")) > MAX_SAFE_USERS:
    raise SystemExit(
        f"LOCUST_USERS depasse la limite de securite ({MAX_SAFE_USERS}). "
        "Augmente MAX_SAFE_USERS volontairement si c'est vraiment voulu."
    )


class PublicVisitor(HttpUser):
    """Simule un visiteur anonyme qui consulte quelques pages publiques."""

    host = os.getenv("BASE_URL", "https://lpb-web-psi.vercel.app")
    # Pause entre deux actions d'un meme utilisateur simule, pour imiter un
    # rythme humain plutot que de marteler le serveur.
    wait_time = between(1, 3)

    @task(5)
    def home(self) -> None:
        self.client.get("/", name="/")

    @task(3)
    def search(self) -> None:
        self.client.get("/recherche", name="/recherche")

    @task(2)
    def workers(self) -> None:
        self.client.get("/travailleurs", name="/travailleurs")

    @task(1)
    def faq(self) -> None:
        self.client.get("/faq", name="/faq")

    @task(1)
    def pricing(self) -> None:
        self.client.get("/tarifs", name="/tarifs")

    @task(1)
    def about(self) -> None:
        self.client.get("/a-propos", name="/a-propos")

    @task(1)
    def contact(self) -> None:
        self.client.get("/contact", name="/contact")

    @task(1)
    def guide(self) -> None:
        self.client.get("/guide", name="/guide")
