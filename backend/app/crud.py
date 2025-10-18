# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .models import Simulation


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


def get_simulation_stats(db: Session):
    # Statistiques globales
    stats = db.query(
        func.avg(Simulation.revenu_mensuel).label("avg_revenu_mensuel"),
        func.avg(Simulation.revenu_de_base).label("avg_revenu_de_base"),
        func.avg(Simulation.revenu_total).label("avg_revenu_total"),
        func.count(Simulation.id).label("total_simulations"),
    ).first()

    # Distribution par statut
    statut_counts = (
        db.query(Simulation.statut, func.count(Simulation.id).label("count"))
        .group_by(Simulation.statut)
        .all()
    )

    # Distribution par nombre d'enfants
    enfants_counts = (db.query(Simulation.nombre_enfants,
                               func.count(Simulation.id).label("count"))
        .group_by(Simulation.nombre_enfants)
        .all()
    )

    return {
        "avg_revenu_mensuel": stats.avg_revenu_mensuel,
        "avg_revenu_de_base": stats.avg_revenu_de_base,
        "avg_revenu_total": stats.avg_revenu_total,
        "total_simulations": stats.total_simulations,
        "statut_distribution": {s[0]: s[1] for s in statut_counts},
        "enfants_distribution": {e[0]: e[1] for e in enfants_counts},
    }
