from pytest_bdd import scenarios, given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app.models import Base

scenarios("../features/simulation.feature")

client = TestClient(app)


@given("un revenu mensuel de 2000 euros")
def revenu_mensuel():
    return 2000.0


@given('un statut "celibataire"')
def statut():
    return "celibataire"


@given("0 enfants")
def nombre_enfants():
    return 0


@when("je lance la simulation")
def simulation(revenu_mensuel, statut, nombre_enfants):
    response = client.post(
        "/simulations/",
        json={
            "revenu_mensuel": revenu_mensuel,
            "statut": statut,
            "nombre_enfants": nombre_enfants,
        },
    )
    return response


@then("le revenu de base doit être 1000 euros")
def revenu_de_base(simulation):
    assert simulation.json()["revenu_de_base"] == 1000


@then("le revenu total doit être 3000 euros")
def revenu_total(simulation):
    assert simulation.json()["revenu_total"] == 3000
