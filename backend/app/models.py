from sqlalchemy import Column, Integer, String, Float
from .database import Base


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(Integer, primary_key=True, index=True)
    revenu_mensuel = Column(Float)
    statut = Column(String)
    nombre_enfants = Column(Integer)
    revenu_de_base = Column(Float)
    revenu_total = Column(Float)
