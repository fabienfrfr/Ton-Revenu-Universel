import pytest
from playwright.sync_api import Page


def test_simulation_e2e(page: Page):
    # Ouvrir la page Streamlit
    page.goto("http://frontend:8501")

    # Remplir le formulaire
    page.fill('input[aria-label="Revenu mensuel actuel (€)"]', "2500")
    page.select_option('select[aria-label="Statut"]', "en couple")
    page.fill('input[aria-label="Nombre d\\\'enfants"]', "2")

    # Cliquer sur le bouton de simulation
    page.click("button:has-text('Lancer la simulation')")

    # Vérifier que les résultats s'affichent
    assert page.is_visible("text=Revenu de base : 1500 €")
    assert page.is_visible("text=Revenu total : 4000 €")

    # Vérifier que les graphiques s'affichent
    assert page.is_visible(".plotly-graph-div")
