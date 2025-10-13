<!--
© 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info

SPDX-License-Identifier: CC-BY-SA-4.0+
SPDX-FileContributor:    Fabien FURFARO
-->

# **📂 Architecture Technique du Simulateur de Revenu de Base**


## 🔧 Composant principaux

###  Calcul du Revenu de Base et du Revenu Total

```mermaid
flowchart LR
    A([Début]) --> B[Recevoir les données :\nrevenu_mensuel, statut, nombre_enfants]
    B --> C{statut == celibataire ?}
    C -->|Oui| D[revenu_de_base = 1000]
    C -->|Non| E[revenu_de_base = 1500]
    D --> F[revenu_de_base += nombre_enfants * 300]
    E --> F
    F --> G[revenu_total = revenu_mensuel + revenu_de_base]
    G --> H[Retourner revenu_de_base et revenu_total]
    H --> I([Fin])
```

## **🔄 Flux de Données**


### **1. Diagramme d'Architecture Globale**
```mermaid
graph LR
  User[Utilisateur] -->|Remplit le formulaire| FE[Streamlit - Frontend]
  subgraph Frontend
    FE
  end
  subgraph Backend
    BE[FastAPI - Backend]
    subgraph Base de Données
      DB[(PostgreSQL)]
    end
  end
  FE -->|POST /simulations/| BE
  BE -->|Lecture/Écriture| DB
  BE -->|Retourne les résultats| FE
  FE -->|Affiche les résultats| User

  style User fill:#f9f,stroke:#333,stroke-width:2px,color:#000
  style FE fill:#bbf,stroke:#333,stroke-width:2px,color:#000
  style BE fill:#bfb,stroke:#333,stroke-width:2px,color:#000
  style DB fill:#fbf,stroke:#333,stroke-width:2px,color:#000
```

---

### **2. Diagramme de Séquence : Simulation d'un Revenu de Base**
```mermaid
sequenceDiagram
    actor Utilisateur
    participant Frontend as Streamlit (Frontend)
    participant Backend as FastAPI (Backend)
    participant DB as PostgreSQL (Base de données)

    Utilisateur->>Frontend: Remplit le formulaire (revenu, statut, enfants)
    Utilisateur->>Frontend: Clique sur "Lancer la simulation"

    Frontend->>Backend: POST /simulations/ (JSON: revenu_mensuel, statut, nombre_enfants)
    activate Backend

    Backend->>DB: Requête SQL : INSERT INTO simulations (revenu_mensuel, statut, nombre_enfants, revenu_de_base, revenu_total)
    activate DB
    DB-->>Backend: Retourne l'ID de la simulation créée
    deactivate DB

    Backend-->>Frontend: Retourne les résultats (JSON: revenu_de_base, revenu_total)
    deactivate Backend

    Frontend->>Utilisateur: Affiche les résultats et les graphiques
```