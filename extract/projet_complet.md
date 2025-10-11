# Project Directory Tree

- ./
  - .gitignore
  - Dockerfile.tests
  - LICENSE
  - Makefile
  - README.md
  - docker-compose.yml
- .pytest_cache/
- .github/
  - workflows/
    - ci-cd.yml
- tests/
  - requirements.txt
  - unit/
    - steps/
      - test_simulation.py
    - features/
      - simulation.feature
  - e2e/
    - conftest.py
    - test_simulation.py
    - __pycache__/
- backend/
  - Dockerfile
  - requirements.txt
  - app/
    - __init__.py
    - crud.py
    - database.py
    - main.py
    - models.py
    - schemas.py
    - __pycache__/
- .vscode/
  - settings.json
- frontend/
  - Dockerfile
  - app.py
  - requirements.txt
- docs/
  - Fiche_projet_SIMUL.pdf
  - archi.md
  - demo.png

---



# File: ./docker-compose.yml
```yaml
version: "3.8"

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db/simulateur
    depends_on:
      db:
        condition: service_healthy

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=simulateur
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d simulateur"]
      interval: 5s
      timeout: 5s
      retries: 5

  tests:
    build:
      context: .
      dockerfile: Dockerfile.tests
    depends_on:
      - backend
      - frontend
    environment:
      - FRONTEND_URL=http://frontend:8501
      - BACKEND_URL=http://backend:8000
    volumes:
      - ./tests:/app/tests
    command: pytest tests/unit tests/e2e -v

volumes:
  postgres_data:

```


# File: ./README.md
```markdown

# Simulateur de Revenu de Base

Un simulateur web moderne pour calculer l'impact d'un revenu de base sur les revenus des ménages, inspiré par les propositions politiques actuelles. Le projet utilise **FastAPI** pour le backend, **Streamlit** pour le frontend, et **pytest-bdd** pour les tests.

![Streamlit Demo](./docs/demo.png)


TODO : 

(à mettre dans la partie doc ? voir les bonnes pratiques de dev)

- vault
- gestion ssh, en cas de serveur

---

## 📌 Fonctionnalités

- **Calcul du revenu de base** selon le statut (célibataire, en couple) et le nombre d'enfants.
- **Visualisation interactive** des résultats avec des graphiques comparatifs (barres, camembert).
- **Base de données SQL** pour stocker les simulations.
- **Tests BDD** avec `pytest-bdd` pour la validation des scénarios.
- **Déploiement automatisé** via GitHub Actions et Docker.

---

## 🛠 Prérequis

- [Docker](https://docs.docker.com/get-docker/) (pour le déploiement local et la production)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.9+](https://www.python.org/downloads/) (pour le développement local)

---

## 🚀 Installation et Lancement

### 1. Cloner le dépôt

```bash
git clone https://github.com/ffurfaro/simulateur_revenu_de_base.git
cd simulateur_revenu_de_base
```

### 2. Lancer avec Docker Compose

```bash
docker-compose up --build
```

- Le **frontend Streamlit** sera disponible à [http://localhost:8501](http://localhost:8501).
- La **documentation FastAPI** sera disponible à [http://localhost:8000/docs](http://localhost:8000/docs).

### 3. Développement local (sans Docker)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou `venv\Scripts\activate` sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 Tests

### Lancer les tests BDD

```bash
cd backend
pytest
```

- Les scénarios BDD sont définis dans `backend/tests/features/`.
- Les étapes de test sont implémentées dans `backend/tests/steps/`.

---

## 📦 Déploiement

### 1. Déploiement local avec Docker Compose

```bash
docker-compose up --build
```

### 2. Déploiement sur un serveur/VM

1. **Configurer les variables d'environnement** (par exemple, `DATABASE_URL`).
2. **Déployer avec Docker Compose** sur ta VM :
   ```bash
   scp docker-compose.yml user@ton-serveur:/chemin/vers/le/projet
   ssh user@ton-serveur
   cd /chemin/vers/le/projet
   docker-compose up -d
   ```
3. **Configurer un reverse proxy** (Nginx, Traefik) pour exposer les ports 80/443.

### 3. CI/CD avec GitHub Actions

- Le workflow `.github/workflows/ci-cd.yml` est configuré pour :
  - Lancer les tests à chaque push/PR.
  - Construire et pousser les images Docker sur Docker Hub.
- **Variables secrètes** :
  - `DOCKER_USERNAME` : Identifiant Docker Hub.
  - `DOCKER_PASSWORD` : Mot de passe ou token Docker Hub.

---

## 📂 Structure du Projet

```
simulateur_revenu_de_base/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI app
│   │   ├── models.py        # Modèles SQLAlchemy
│   │   ├── schemas.py       # Schémas Pydantic
│   │   ├── crud.py          # Logique CRUD
│   │   └── database.py      # Configuration de la base de données
│   ├── tests/
│   │   ├── features/        # Fichiers BDD (Gherkin)
│   │   └── steps/           # Étapes pytest-bdd
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── app.py               # Streamlit app
│   └── Dockerfile
|
├── tests/
│   ├── unit/                # Tests unitaires/BDD pour le backend
│   │   ├── features/
│   │   └── steps/
│   ├── e2e/                 # Tests end-to-end (frontend + backend)
│   │   ├── test_simulation.py
│   │   └── conftest.py
│   └── requirements.txt     # Dépendances spécifiques aux tests
|
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pour CI/CD
│
├── docker-compose.yml
|
└── README.md
```

---

## 🔧 Configuration

### Variables d'environnement

| Variable          | Description                          | Exemple de valeur                     |
|-------------------|--------------------------------------|---------------------------------------|
| `DATABASE_URL`    | URL de la base de données PostgreSQL | `postgresql://user:pass@db:5432/db`   |

---

## 📊 Exemples de Visualisations

### 1. Comparaison des revenus (graphique en barres)
![Bar Chart](https://via.placeholder.com/400x200?text=Bar+Chart) *(TODO)*

### 2. Répartition des revenus (graphique camembert)
![Pie Chart](https://via.placeholder.com/400x200?text=Pie+Chart) *(TODO)*

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment contribuer :

1. **Fork** le dépôt.
2. Crée une **branche** pour ta fonctionnalité (`git checkout -b ma-nouvelle-fonctionnalite`).
3. **Commit** tes changements (`git commit -am 'Ajout d'une nouvelle fonctionnalité'`).
4. **Push** la branche (`git push origin ma-nouvelle-fonctionnalite`).
5. Ouvre une **Pull Request**.

---

## 📜 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 📬 Contact

Pour toute question ou suggestion, contacte-moi à [fabien.furfaro@gail.com](mailto:fabien.furfaro@example.com).
```


# File: ./Makefile
```text
.PHONY: install lint coverage merge-dev delete-ci-runs

lint:
	isort src/ tests/
	python -m pylint src/ tests/

coverage:
	pytest --cov=src --cov-report=term-missing

COMMIT_MESSAGE ?= "Merge dev into main"

merge-dev:
	git checkout main
	git merge --squash dev
	git commit -m $(COMMIT_MESSAGE)
	git push origin main
	git branch -D dev
	git checkout -b dev main
	git push origin dev --force

delete-ci-runs:
	@echo "Deleting all GitHub Actions runs from GitHub CLI..."
	gh run list --limit 1000 --json databaseId -q '.[].databaseId' | xargs -n 1 gh run delete
```


# File: ./LICENSE
```text
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/
```


# File: ./Dockerfile.tests
```text
FROM python:3.9

WORKDIR /app

# Installer les dépendances système pour Playwright
RUN apt-get update && apt-get install -y \
    wget \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY tests/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Installer Playwright et ses navigateurs
RUN playwright install

# Copier les tests
COPY tests/ /app/tests/

ENTRYPOINT ["pytest"]

```


# File: ./.gitignore
```text
__pycache__/
.pytest_cache/
.mypy_cache/
*.pyc
*.pyo
.env
.ipynb_checkpoints/
.coverage
.git

*.db
```


# File: ./.github/workflows/ci-cd.yml
```yaml
name: CI/CD Pipeline

on:
    push:
        branches: [main]
    pull_request:
        branches: [main]

jobs:
    test-unit:
        runs-on: ubuntu-latest
        services:
            postgres:
                image: postgres:13
                env:
                    POSTGRES_USER: user
                    POSTGRES_PASSWORD: password
                    POSTGRES_DB: simulateur
                ports:
                    - 5432:5432
                options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

        steps:
            - uses: actions/checkout@v2
            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                  python-version: "3.9"
            - name: Install dependencies
              run: |
                  python -m pip install --upgrade pip
                  pip install -r backend/requirements.txt
                  pip install -r tests/requirements.txt
            - name: Run unit tests
              env:
                  DATABASE_URL: postgresql://user:password@localhost/simulateur
              run: |
                  pytest tests/unit -v

    test-e2e:
        needs: test-unit
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - name: Set up Python
              uses: actions/setup-python@v2
              with:
                  python-version: "3.9"
            - name: Install dependencies
              run: |
                  python -m pip install --upgrade pip
                  pip install -r tests/requirements.txt
                  playwright install
            - name: Start services
              run: |
                  docker-compose up -d db backend frontend
                  sleep 10  # Attendre que les services soient prêts
            - name: Run E2E tests
              run: |
                  pytest tests/e2e -v
            - name: Stop services
              if: always()
              run: |
                  docker-compose down

```


# File: ./tests/requirements.txt
```text
pytest
pytest-bdd
pytest-playwright
playwright
requests

```


# File: ./tests/unit/steps/test_simulation.py
```python
from pytest_bdd import scenarios, given, when, then
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal, engine
from backend.app.models import Base

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

```


# File: ./tests/unit/features/simulation.feature
```text
Feature: Simulation de revenu de base
  Scenario: Calculer le revenu de base pour un célibataire sans enfant
    Given un revenu mensuel de 2000 euros
    And un statut "celibataire"
    And 0 enfants
    When je lance la simulation
    Then le revenu de base doit être 1000 euros
    And le revenu total doit être 3000 euros

```


# File: ./tests/e2e/conftest.py
```python
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # headless=True pour la CI
        yield browser
        browser.close()


@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

```


# File: ./tests/e2e/test_simulation.py
```python
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

```


# File: ./backend/Dockerfile
```text
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

```


# File: ./backend/requirements.txt
```text
fastapi
uvicorn
sqlalchemy
pytest
pytest-bdd
pydantic
```


# File: ./backend/app/crud.py
```python
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

```


# File: ./backend/app/database.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./simulateur.db"  # ou "postgresql://user:password@postgresserver/db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

```


# File: ./backend/app/schemas.py
```python
from pydantic import BaseModel


class SimulationCreate(BaseModel):
    revenu_mensuel: float
    statut: str
    nombre_enfants: int


class SimulationResponse(SimulationCreate):
    id: int
    revenu_de_base: float
    revenu_total: float

```


# File: ./backend/app/__init__.py
```python

```


# File: ./backend/app/main.py
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/simulations/", response_model=schemas.SimulationResponse)
def create_simulation(
    simulation: schemas.SimulationCreate, db: Session = Depends(get_db)
):
    return crud.create_simulation(db=db, simulation=simulation)

```


# File: ./backend/app/models.py
```python
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

```


# File: ./.vscode/settings.json
```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```


# File: ./frontend/app.py
```python
import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Simulateur de Revenu de Base")

# Barre latérale pour les paramètres
with st.sidebar:
    st.header("Paramètres")
    revenu_mensuel = st.number_input(
        "Revenu mensuel actuel (€)", min_value=0.0, value=2000.0
    )
    statut = st.selectbox("Statut", ["célibataire", "en couple"])
    nombre_enfants = st.number_input("Nombre d'enfants", min_value=0, value=0)

# Bouton de simulation
if st.button("Lancer la simulation", type="primary"):
    response = requests.post(
        "http://backend:8000/simulations/",
        json={
            "revenu_mensuel": revenu_mensuel,
            "statut": statut,
            "nombre_enfants": nombre_enfants,
        },
    )
    if response.status_code == 200:
        result = response.json()
        revenu_de_base = result["revenu_de_base"]
        revenu_total = result["revenu_total"]

        # Affichage des résultats
        st.success(f"Revenu de base : **{revenu_de_base} €**")
        st.success(f"Revenu total après application : **{revenu_total} €**")

        # Création d'un DataFrame pour les graphiques
        data = {
            "Catégorie": ["Revenu actuel", "Revenu de base", "Revenu total"],
            "Montant (€)": [revenu_mensuel, revenu_de_base, revenu_total],
        }
        df = pd.DataFrame(data)

        # Graphique comparatif
        fig = px.bar(
            df,
            x="Catégorie",
            y="Montant (€)",
            title="Comparaison des revenus",
            color="Catégorie",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Graphique camembert
        fig_pie = px.pie(
            df, values="Montant (€)", names="Catégorie", title="Répartition des revenus"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.error("Erreur lors de la simulation. Veuillez réessayer.")

# Exemple de simulation automatique pour illustration
if st.checkbox("Voir un exemple de simulation"):
    exemple = {"revenu_mensuel": 2500, "statut": "en couple", "nombre_enfants": 2}
    response = requests.post("http://backend:8000/simulations/", json=exemple)
    if response.status_code == 200:
        result = response.json()
        df_exemple = pd.DataFrame(
            {
                "Catégorie": ["Revenu actuel", "Revenu de base", "Revenu total"],
                "Montant (€)": [
                    exemple["revenu_mensuel"],
                    result["revenu_de_base"],
                    result["revenu_total"],
                ],
            }
        )
        fig_exemple = px.bar(
            df_exemple,
            x="Catégorie",
            y="Montant (€)",
            title="Exemple : Couple avec 2 enfants",
        )
        st.plotly_chart(fig_exemple, use_container_width=True)

```


# File: ./frontend/Dockerfile
```text
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

```


# File: ./frontend/requirements.txt
```text
streamlit
plotly
pandas
requests

```


# File: ./docs/archi.md
```markdown
## Architecture fonctionnelle

Inclu les éléments techniques

```mermaid

graph LR

  User[Utilisateur] --> FE[Streamlit - Interface utilisateur]
  subgraph Frontend
    FE
  end
  subgraph Backend
    BE[FastAPI - API métier]
    subgraph ERD
      DB[(PostgreSQL - Base de données)]
    end
  end
  FE -- Envoi des données de simulation (POST /simulations/) --> BE
  BE -- Lecture / écriture des données de simulation --> DB
  BE -- Renvoi des résultats au frontend --> FE

 

  style User fill:#f9f,stroke:#333,stroke-width:2px,color:#000
  style FE fill:#bbf,stroke:#333,stroke-width:2px,color:#000
  style BE fill:#bfb,stroke:#333,stroke-width:2px,color:#000
  style DB fill:#fbf,stroke:#333,stroke-width:2px,color:#000

  linkStyle 0 stroke:#f66,stroke-width:2px
  linkStyle 1 stroke:#6f6,stroke-width:2px
  linkStyle 2 stroke:#66f,stroke-width:2px

 

```

 
```
