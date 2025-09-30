from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SimulationParams(BaseModel):
    current_income: float
    household_size: int


@app.post("/api/calculate_basic_income")
def calculate_basic_income(params: SimulationParams):
    # Basic income logic:
    # For example: base 1000 €/person, minus 10% of current income, minimum 0
    amount = max(params.household_size * 1000 - 0.1 * params.current_income, 0)
    return {"basic_income": amount}
