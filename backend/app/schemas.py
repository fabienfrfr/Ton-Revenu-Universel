from pydantic import BaseModel


class SimulationCreate(BaseModel):
    revenu_mensuel: float
    statut: str
    nombre_enfants: int


class SimulationResponse(SimulationCreate):
    id: int
    revenu_de_base: float
    revenu_total: float
