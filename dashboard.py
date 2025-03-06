import sqlite3
import streamlit as st

# 🏆 Configurer la page
st.set_page_config(page_title="Dashboard ESG - Orange", page_icon="📊", layout="wide")

# 📌 Connexion à la base de données
def get_connection():
    return sqlite3.connect("database.db")

# 📌 Dictionnaire de correspondance entre entités et noms des tables SQL
entity_mapping = {
    "Catégorie": "categories_parties_prenantes",
    "Maillon": "maillons",
    "IRO": "iros",
    "Plan d'action": "plans_actions",
    "Enjeu": "enjeux"
}

# 📌 Fonction pour récupérer les données
def get_entities(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, nom FROM {table_name}")
    entities = cursor.fetchall()
    conn.close()
    return {id: nom for id, nom in entities}

# 📌 Fonction pour ajouter une entité
def add_entity(table_name, values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO {table_name} (nom) VALUES (?)", (values,))
    conn.commit()
    conn.close()

# 📌 Fonction pour modifier une entité
def update_entity(table_name, entity_id, new_value):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET nom = ? WHERE id = ?", (new_value, entity_id))
    conn.commit()
    conn.close()

# 📌 Fonction pour supprimer une entité
def delete_entity(table_name, entity_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (entity_id,))
    conn.commit()
    conn.close()

# 📌 Sélection du Mode
mode_selection = st.sidebar.radio("🔎 Sélectionnez un Mode :", ["Ajouter des Données", "Gérer les Relations"])

# ------------------ 🔹 Mode : Ajouter des Données ------------------
if mode_selection == "Ajouter des Données":
    entity_type = st.sidebar.selectbox("📌 Sélectionnez une section :", list(entity_mapping.keys()))
    table_name = entity_mapping[entity_type]

    st.header(f"📝 Ajouter une {entity_type}")

    with st.form(key=f"form_{entity_type}"):
        entity_name = st.text_input(f"📌 Nom de la {entity_type} :")
        submitted = st.form_submit_button("✅ Ajouter")

    if submitted and entity_name:
        add_entity(table_name, entity_name)
        st.success(f"✅ {entity_type} '{entity_name}' ajoutée avec succès !")
        st.rerun()

    # 📌 Afficher les éléments existants
    entities = get_entities(table_name)
    if entities:
        st.subheader(f"📋 {entity_type}s existants :")

        for entity_id, entity_name in entities.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.text(entity_name)

            # Modifier une entité
            if col2.button("Modifier", key=f"mod_{entity_id}"):
                new_value = st.text_input("Nouvelle valeur :", entity_name, key=f"new_val_{entity_id}")
                if st.button("Sauvegarder", key=f"save_{entity_id}"):
                    update_entity(table_name, entity_id, new_value)
                    st.success(f"✅ {entity_type} '{entity_name}' mise à jour avec succès !")
                    st.rerun()

            # Supprimer une entité
            if col3.button("❌", key=f"del_{entity_id}"):
                delete_entity(table_name, entity_id)
                st.warning(f"🚨 {entity_type} '{entity_name}' supprimée !")
                st.rerun()

# ------------------ 🔹 Mode : Gérer les Relations ------------------
elif mode_selection == "Gérer les Relations":
    st.sidebar.markdown("🔗 **Gérer les Relations**")
    relation_action = st.sidebar.radio("📌 Sélectionnez une Relation :", ["Associer un Maillon à une Catégorie"])

    if relation_action == "Associer un Maillon à une Catégorie":
        st.header("🔗 Associer un Maillon à une Catégorie")

        maillons = get_entities("maillons")
        categories = get_entities("categories_parties_prenantes")

        if maillons and categories:
            selected_maillon = st.selectbox("📌 Sélectionnez un Maillon :", list(maillons.values()))
            selected_categorie = st.selectbox("📌 Sélectionnez une Catégorie :", list(categories.values()))

            if st.button("✅ Associer", key="associer_maillon_categorie"):
                st.success(f"✅ '{selected_maillon}' a été associé à '{selected_categorie}' avec succès !")
        else:
            st.warning("⚠️ Aucun Maillon ou Catégorie disponible. Ajoutez des données d'abord !")
