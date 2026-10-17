"""Donnees attendues, separees de la logique des tests."""
from __future__ import annotations

from datetime import date

from framework.pages.public_pages import (
    AboutPage,
    ContactPage,
    FaqPage,
    GuidePage,
    HomePage,
    LoginPage,
    PricingPage,
    RegisterPage,
    SearchPage,
    WorkersPage,
)
from framework.pages.worker_pages import (
    AnnualStatementPage,
    WorkerBillingPage,
    WorkerDashboardPage,
    WorkerMessagesPage,
    WorkerNotificationsPage,
    WorkerPayoutsPage,
    WorkerPlanPage,
    WorkerProfilePage,
    WorkerSearchPage,
)

# --- site public ------------------------------------------------------
PUBLIC_PAGES = [
    (HomePage, "On Bricole"),
    (AboutPage, "À propos"),
    (FaqPage, "Foire aux questions"),
    (PricingPage, "Forfaits"),
    (GuidePage, "Guide"),
    (ContactPage, "Contactez-nous"),
    (SearchPage, "On Bricole"),
    (WorkersPage, "Travailleurs"),
    (LoginPage, "Connexion"),
    (RegisterPage, "Créer un compte"),
]
HEADER_LINKS = ["/recherche", "/travailleurs", "/a-propos", "/faq", "/tarifs", "/login",
                "/register"]
FOOTER_LINKS = ["/guide", "/contact", "/conditions", "/confidentialite",
                "/suppression-des-donnees"]

# --- espace travailleur -----------------------------------------------
WORKER_PAGES = [
    WorkerDashboardPage, WorkerSearchPage, WorkerMessagesPage, WorkerProfilePage,
    WorkerPayoutsPage, WorkerBillingPage, WorkerPlanPage, WorkerNotificationsPage,
    AnnualStatementPage,
]
WORKER_NAV_LINKS = ["/worker/search", "/worker/candidatures", "/worker/travaux",
                    "/worker/demandes", "/worker/messages"]
WORKER_NAV_LABELS = ["Tableau de bord", "Boulots", "Candidatures", "Travaux", "Mes demandes",
                     "Messagerie"]
USER_MENU_HREFS = ["/worker", "/worker/profil", "/worker/payouts", "/worker/facturation", "/"]
DASHBOARD_SECTIONS = {"Conversations", "Notifications"}
RADIUS_OPTIONS = ["5 km", "10 km", "25 km", "50 km"]
PRICING_MODES = ["—", "Horaire", "Forfait", "Négociable"]
WORKER_TYPES = ["Occasionnel", "Permanent"]
PROFILE_TABS = ("Informations personnelles", "Disponibilités", "Paramètres du compte",
                "Vérification d’identité")
PLAN_BUTTONS = ["Passer à Permanent", "Passer à Permanent Plus"]
CURRENT_YEAR = str(date.today().year)
PREVIOUS_YEAR = str(date.today().year - 1)
