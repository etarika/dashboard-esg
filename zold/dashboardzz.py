import streamlit as st
import pandas as pd
import plotly.express as px

# Données des parties prenantes
data = {
    "Maillon": ["Approvisionnement", "Approvisionnement", "Infrastructure", "Infrastructure", "Services", "Services", "Recyclage", "Recyclage"],
    "Partie_Prenante": ["Fournisseurs", "Investisseurs", "Régulateurs", "Distributeurs", "Clients", "Partenaires Tech", "ONG & Associations", "Autorités Environnementales"],
    "IRO": ["Risque ESG", "Opportunité Marché", "Risque Réglementaire", "Optimisation Logistique", "Expérience Client", "Innovation Digitale", "Économie Circulaire", "Normes Environnementales"],
    "Influence": [3, 3, 4, 2, 4, 3, 2, 4],
    "Attentes": [2, 3, 4, 2, 3, 4, 4, 3],
    "Impact_Financier": [500, 700, 1200, 600, 800, 950, 400, 650],
    "Impact_Environnemental": [80, 60, 100, 50, 90, 70, 120, 110],
}

df = pd.DataFrame(data)

# Interface Streamlit avec un menu latéral
st.title("📊 Dashboard Interactif - Orange")

menu = st.sidebar.radio("📌 Sélectionnez une section :", ["Vue d'ensemble", "Matrice Parties Prenantes", "Filtrage Avancé"])

# 📍 Section 1 : Vue Générale
if menu == "Vue d'ensemble":
    st.header("📌 Vue Générale des Indicateurs")
    st.write("🔎 **Ajoute ici les autres graphiques et analyses.**")

# 📍 Section 2 : Matrice Parties Prenantes
elif menu == "Matrice Parties Prenantes":
    st.header("🎯 Matrice Parties Prenantes - Influence vs Attentes")

    # Sélection du Maillon
    maillon_selected = st.selectbox("📌 Sélectionnez un Maillon", df["Maillon"].unique())

    # Filtrage des données
    df_filtered = df[df["Maillon"] == maillon_selected]

    # Création de la matrice interactive
    fig = px.scatter(df_filtered, x="Attentes", y="Influence", text="Partie_Prenante",
                     title=f"Matrice Influence vs Attentes - {maillon_selected}",
                     labels={"Influence": "Influence des Parties Prenantes", "Attentes": "Attentes des Parties Prenantes"},
                     range_x=[0.5, 4.5], range_y=[0.5, 4.5],
                     size_max=15)

    fig.update_traces(textposition='top center', marker=dict(size=12, opacity=0.7))

    # Affichage de la matrice interactive
    st.plotly_chart(fig)

    # Affichage du tableau filtré
    st.write("📊 **Données filtrées :**")
    st.dataframe(df_filtered)

# 📍 Section 3 : Filtrage Avancé
elif menu == "Filtrage Avancé":
    st.header("🔎 Analyse des Parties Prenantes par Maillon, Partie Prenante et IRO")

    # Sélection des filtres
    maillon_selected = st.selectbox("📌 Filtrer par Maillon :", ["Tous"] + list(df["Maillon"].unique()))
    partie_prenante_selected = st.selectbox("📌 Filtrer par Partie Prenante :", ["Toutes"] + list(df["Partie_Prenante"].unique()))
    iro_selected = st.selectbox("📌 Filtrer par IRO :", ["Tous"] + list(df["IRO"].unique()))

    # Appliquer les filtres
    df_filtered = df.copy()
    if maillon_selected != "Tous":
        df_filtered = df_filtered[df_filtered["Maillon"] == maillon_selected]
    if partie_prenante_selected != "Toutes":
        df_filtered = df_filtered[df_filtered["Partie_Prenante"] == partie_prenante_selected]
    if iro_selected != "Tous":
        df_filtered = df_filtered[df_filtered["IRO"] == iro_selected]

    # Affichage du tableau filtré
    st.write("📊 **Données filtrées :**")
    st.dataframe(df_filtered)

    # Graphique d'impact
    if not df_filtered.empty:
        fig = px.bar(df_filtered, x="Partie_Prenante", y=["Impact_Financier", "Impact_Environnemental"],
                     title="📉 Impact Financier & Environnemental par Partie Prenante",
                     labels={"value": "Impact", "variable": "Type d'Impact"},
                     barmode="group")

        st.plotly_chart(fig)
    else:
        st.warning("⚠️ Aucune donnée trouvée avec ces filtres.")

import sqlite3

# Connexion à la base SQLite (créée si elle n'existe pas)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Création de la table (si elle n'existe pas encore)
cursor.execute('''
CREATE TABLE IF NOT EXISTS parties_prenantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maillon TEXT,
    partie_prenante TEXT,
    iro TEXT,
    influence INTEGER,
    attentes INTEGER,
    impact_financier REAL,
    impact_environnemental REAL
)
''')

conn.commit()
conn.close()


import streamlit as st
import sqlite3
import pandas as pd

# 📌 Fonction pour ajouter une entrée dans la base
def ajouter_donnees(maillon, partie_prenante, iro, influence, attentes, impact_financier, impact_environnemental):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO parties_prenantes (maillon, partie_prenante, iro, influence, attentes, impact_financier, impact_environnemental)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (maillon, partie_prenante, iro, influence, attentes, impact_financier, impact_environnemental))
    conn.commit()
    conn.close()

# 📌 Interface Streamlit
st.title("📝 Ajout de Parties Prenantes")

with st.form("ajout_donnees"):
    maillon = st.selectbox("📌 Sélectionnez un Maillon :", ["Approvisionnement", "Infrastructure", "Services", "Recyclage"])
    partie_prenante = st.text_input("👤 Nom de la Partie Prenante :")
    iro = st.text_input("⚖️ IRO (Impact/Risque/Opportunité) :")
    influence = st.slider("📊 Influence (1 à 4) :", 1, 4, 2)
    attentes = st.slider("🎯 Attentes (1 à 4) :", 1, 4, 2)
    impact_financier = st.number_input("💰 Impact Financier :", min_value=0, step=100)
    impact_environnemental = st.number_input("🌱 Impact Environnemental :", min_value=0, step=10)
    
    submitted = st.form_submit_button("✅ Ajouter les Données")

    if submitted:
        ajouter_donnees(maillon, partie_prenante, iro, influence, attentes, impact_financier, impact_environnemental)
        st.success("✅ Données ajoutées avec succès !")


# 📌 Fonction pour récupérer les données
def recuperer_donnees():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM parties_prenantes", conn)
    conn.close()
    return df

# 📌 Affichage des données
st.header("📊 Parties Prenantes en Base")
df = recuperer_donnees()
df_editable = st.data_editor(df)

# 📌 Mise à jour des données après édition
if st.button("💾 Enregistrer les modifications"):
    conn = sqlite3.connect("database.db")
    df_editable.to_sql("parties_prenantes", conn, if_exists="replace", index=False)
    conn.close()
    st.success("✅ Modifications enregistrées !")


