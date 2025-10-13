# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

import streamlit as st
import requests
import pandas as pd
import plotly.express as px


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Simulateur Revenu Universel",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.revenudebase.info/help",
        "Report a bug": "mailto:fabien.furfaro@gmail.com",
        "About": "# Simulateur Revenu de Base\nVersion 1.0",
    },
)

local_css("style.css")

st.title("📊 Simulateur de Revenu Universel")

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
