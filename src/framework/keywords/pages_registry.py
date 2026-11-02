"""Association nom (string, pour le JSON) -> classe de page.

Un futur frontend proposera ces noms dans une liste deroulante ; pour en ajouter un,
importer la classe et l'ajouter ici (aucune autre modification necessaire).
"""
from __future__ import annotations

from framework.pages.base_page import BasePage
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
    WorkerRequestsPage,
    WorkerSearchPage,
)

PAGE_REGISTRY: dict[str, type[BasePage]] = {
    cls.__name__: cls
    for cls in (
        HomePage, AboutPage, FaqPage, PricingPage, GuidePage, ContactPage,
        SearchPage, WorkersPage, LoginPage, RegisterPage,
        WorkerDashboardPage, WorkerSearchPage, WorkerMessagesPage, WorkerProfilePage,
        WorkerPayoutsPage, WorkerBillingPage, WorkerPlanPage, WorkerNotificationsPage,
        AnnualStatementPage, WorkerRequestsPage,
    )
}


def resolve_page(name: str) -> type[BasePage]:
    try:
        return PAGE_REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"Page inconnue : '{name}'. Disponibles : {sorted(PAGE_REGISTRY)}"
        ) from None
