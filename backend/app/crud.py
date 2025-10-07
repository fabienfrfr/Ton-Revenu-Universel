from sqlalchemy.orm import Session
from . import models, schemas


def create_simulation(db: Session, simulation: schemas.SimulationCreate):
    revenu_de_base = 1000 if simulation.statut == "celibataire" else 1500
    revenu_de_base += simulation.nombre_enfants * 300
    revenu_total = simulation.revenu_mensuel + revenu_de_base

    db_simulation = models.Simulation(
        revenu_mensuel=simulation.revenu_mensuel,
        statut=simulation.statut,
        nombre_enfants=simulation.nombre_enfants,
        revenu_de_base=revenu_de_base,
        revenu_total=revenu_total,
    )
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation
