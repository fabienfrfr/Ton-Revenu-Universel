# TRU
Ton Revenu Universel (Basic Income Simulator)

```
basic_income_simulator/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```


## Prerequisites

- Docker and docker-compose installed
- Python 3.10+ for local runs

## Running locally without Docker

1. Backend:

```

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

```

2. Frontend:

```

cd frontend
pip install -r requirements.txt
streamlit run app.py

```

Note: For testing locally, change the URL `http://backend:8000/...` in `frontend/app.py` to `http://localhost:8000/api/calculate_basic_income`.

---

## Running with Docker

```

docker-compose up --build

```

- Backend API accessible at http://localhost:8000
- Frontend accessible at http://localhost:8501

---

## Deployment Suggestions

- Deploy backend on a cloud VM or container service (AWS, Azure, DigitalOcean).
- Deploy frontend on Streamlit Cloud or as a container.
- Modify API endpoint in frontend to your cloud backend URL.