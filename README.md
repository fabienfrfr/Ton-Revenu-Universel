
# Simulateur de Revenu de Base

Un simulateur web moderne pour calculer l'impact d'un revenu de base sur les revenus des ménages, inspiré par les propositions politiques actuelles. Le projet utilise **FastAPI** pour le backend, **Streamlit** pour le frontend, et **pytest-bdd** pour les tests.

![Streamlit Demo](./docs/demo_simul.png)

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