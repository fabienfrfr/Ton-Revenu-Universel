# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Fabien FURFARO

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:
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

st.title("📊 Simulateur de Revenu Universel (en cours de développement)")

# Bloc horizontal pour les paramètres en haut, colonne par colonne
col1, col2, col3, col_button = st.columns([2, 2, 2, 1])

with col1:
    revenu_mensuel = st.number_input(
        "Revenu mensuel actuel (€)", min_value=0.0, value=2000.0
    )

with col2:
    statut = st.selectbox("Statut", ["célibataire", "en couple"])

with col3:
    nombre_enfants = st.number_input("Nombre d'enfants", min_value=0, value=0)

with col_button:
    lancer_simulation = st.button("Lancer la simulation", type="primary")

if lancer_simulation:
    response = requests.post(
        "http://backend:8000/simulations/",
        json={
            "revenu_mensuel": revenu_mensuel,
            "statut": statut,
            "nombre_enfants": nombre_enfants,
        },
        timeout=10,  # Set a timeout of 10 seconds
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

        # Création des onglets pour les graphiques
        tab1, tab2 = st.tabs(["Graphique barres", "Statistiques globales"])

        with tab1:
            fig = px.bar(
                df,
                x="Catégorie",
                y="Montant (€)",
                title="Comparaison des revenus",
                color="Catégorie",
            )
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("📊 Statistiques globales")
            stats_response = requests.get(
                "http://backend:8000/simulations/stats", timeout=10
            )
            if stats_response.status_code == 200:
                stats = stats_response.json()
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Nombre total de simulations", stats["total_simulations"])
                    st.metric(
                        "Revenu mensuel moyen", f"{stats['avg_revenu_mensuel']:.2f} €"
                    )
                    st.metric(
                        "Revenu de base moyen", f"{stats['avg_revenu_de_base']:.2f} €"
                    )
                    st.metric(
                        "Revenu total moyen", f"{stats['avg_revenu_total']:.2f} €"
                    )
                with col2:
                    st.write("### Répartition par statut")
                    statut_df = pd.DataFrame(
                        list(stats["statut_distribution"].items()),
                        columns=["Statut", "Nombre"],
                    )
                    fig_statut = px.bar(
                        statut_df,
                        x="Statut",
                        y="Nombre",
                        title="Nombre de simulations par statut",
                        color="Statut",
                    )
                    st.plotly_chart(fig_statut, use_container_width=True)
                    st.write("### Répartition par nombre d'enfants")
                    enfants_df = pd.DataFrame(
                        list(stats["enfants_distribution"].items()),
                        columns=["Enfants", "Nombre"],
                    )
                    fig_enfants = px.bar(
                        enfants_df,
                        x="Enfants",
                        y="Nombre",
                        title="Nombre de simulations par nombre d'enfants",
                        color="Enfants",
                    )
                    st.plotly_chart(fig_enfants, use_container_width=True)
            else:
                st.error("Impossible de récupérer les statistiques.")

    else:
        st.error("Erreur lors de la simulation. Veuillez réessayer.")

# Exemple de simulation automatique pour illustration
if st.checkbox("Voir un exemple de simulation"):
    exemple = {"revenu_mensuel": 2500, "statut": "en couple", "nombre_enfants": 2}
    response = requests.post(
        "http://backend:8000/simulations/", json=exemple, timeout=10
    )
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
