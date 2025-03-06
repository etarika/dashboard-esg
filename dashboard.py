import sqlite3
import streamlit as st

# 🏆 Configurer la page
st.set_page_config(
    page_title="Dashboard ESG - Orange",
    page_icon="📊",
    layout="wide"
)

# 📌 Afficher le logo et le titre dans la barre latérale
with st.sidebar:
    st.image("logo_orange.gif", width=100)
    st.markdown("## 📊 Dashboard ESG - Orange")
    st.write("Bienvenue sur le tableau de bord interactif.")

# 📌 Affichage du reste du contenu
st.markdown("---")

# 📌 Fonctions pour interagir avec la base de données
def ajouter_categorie(nom):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO categories_parties_prenantes (nom) VALUES (?)", (nom,))
    conn.commit()
    conn.close()

def ajouter_maillon(nom, description):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO maillons (nom, description) VALUES (?, ?)", (nom, description))
    conn.commit()
    conn.close()

def get_maillons():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM maillons")
    maillons = cursor.fetchall()
    conn.close()
    return {nom: id for id, nom in maillons}

def get_categories():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM categories_parties_prenantes")
    categories = cursor.fetchall()
    conn.close()
    return {nom: id for id, nom in categories}

def ajouter_iro(numero, description, type_iro, type_materialite):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO iros (numero, description, type, type_materialite) VALUES (?, ?, ?, ?)", 
                   (numero, description, type_iro, type_materialite))
    conn.commit()
    conn.close()

def ajouter_plan_action(numero, type_plan, description):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO plans_actions (numero, type, description) VALUES (?, ?, ?)", 
                   (numero, type_plan, description))
    conn.commit()
    conn.close()

def ajouter_enjeu(numero, description, materialite):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO enjeux (numero, description, materialite) VALUES (?, ?, ?)", 
                   (numero, description, materialite))
    conn.commit()
    conn.close()

# 📌 Interface Streamlit
st.title("📊 Gestion des Données")

# 📌 Sélection du Mode (Ajout ou Relation)
st.sidebar.markdown("📌 **Navigation**")
mode_selection = st.sidebar.radio(
    "🔎 Sélectionnez un Mode :", [
        "Ajouter des Données", 
        "Gérer les Relations"
    ]
)

# ------------------ 🔹 Mode : Ajouter des Données ------------------
if mode_selection == "Ajouter des Données":
    action = st.sidebar.radio(
        "📌 Sélectionnez une section :",
        [
            "Ajouter une Catégorie",
            "Ajouter un Maillon",
            "Ajouter un IRO",
            "Ajouter un Plan d'Action",
            "Ajouter un Enjeu"
        ]
    )

    # 📌 Ajouter une Catégorie
    if action == "Ajouter une Catégorie":
        st.header("📝 Ajouter une Catégorie de Partie Prenante")
        with st.form(key="form_categorie"):
            nom_categorie = st.text_input("📌 Nom de la Catégorie :")
            submitted = st.form_submit_button("✅ Ajouter")
        
        if submitted and nom_categorie:
            ajouter_categorie(nom_categorie)
            st.success(f"✅ Catégorie '{nom_categorie}' ajoutée avec succès !")
            st.rerun()

        categories = get_categories()
        if categories:
            st.subheader("📋 Catégories existantes :")
            st.write("\n".join([f"- {nom}" for nom in categories.keys()]))
        else:
            st.warning("⚠️ Aucune catégorie enregistrée.")

    # 📌 Ajouter un Maillon
    elif action == "Ajouter un Maillon":
        st.header("📝 Ajouter un Maillon")
        with st.form(key="form_maillon"):
            nom_maillon = st.text_input("📌 Nom du Maillon :")
            description_maillon = st.text_area("📖 Description du Maillon :")
            submitted = st.form_submit_button("✅ Ajouter")

        if submitted and nom_maillon and description_maillon:
            ajouter_maillon(nom_maillon, description_maillon)
            st.success(f"✅ Maillon '{nom_maillon}' ajouté avec succès !")
            st.rerun()

        maillons = get_maillons()
        if maillons:
            st.subheader("📋 Maillons existants :")
            for nom in maillons.keys():
                st.markdown(f"- {nom}")
        else:
            st.warning("⚠️ Aucun maillon enregistré.")

    # 📌 Ajouter un IRO
    elif action == "Ajouter un IRO":
        st.header("📝 Ajouter un IRO")
        with st.form(key="form_iro"):
            numero_iro = st.number_input("🔢 Numéro de l'IRO :", min_value=1, step=1)
            description_iro = st.text_area("📖 Description de l'IRO :")
            type_iro = st.selectbox("📌 Type d'IRO :", ["Impact", "Risque", "Opportunité"])
            type_materialite = st.selectbox("📌 Type de Matérialité :", ["Environnement", "Social", "Gouvernance"])
            submitted = st.form_submit_button("✅ Ajouter")

        if submitted and description_iro:
            ajouter_iro(numero_iro, description_iro, type_iro, type_materialite)
            st.success(f"✅ IRO #{numero_iro} ajouté avec succès !")

    # 📌 Ajouter un Plan d'Action
    elif action == "Ajouter un Plan d'Action":
        st.header("📝 Ajouter un Plan d'Action")
        with st.form(key="form_plan"):
            numero_plan = st.number_input("🔢 Numéro du Plan :", min_value=1, step=1)
            type_plan = st.selectbox("📌 Type de Plan :", ["Stratégique", "Opérationnel", "Correctif"])
            description_plan = st.text_area("📖 Description du Plan :")
            submitted = st.form_submit_button("✅ Ajouter")

        if submitted and description_plan:
            ajouter_plan_action(numero_plan, type_plan, description_plan)
            st.success(f"✅ Plan d'Action #{numero_plan} ajouté avec succès !")

    # 📌 Ajouter un Enjeu
    elif action == "Ajouter un Enjeu":
        st.header("📝 Ajouter un Enjeu")
        with st.form(key="form_enjeu"):
            numero_enjeu = st.number_input("🔢 Numéro de l'Enjeu :", min_value=1, step=1)
            description_enjeu = st.text_area("📖 Description de l'Enjeu :")
            materialite = st.selectbox("📌 Matérialité de l'Enjeu :", ["Faible", "Moyenne", "Élevée"])
            submitted = st.form_submit_button("✅ Ajouter")

        if submitted and description_enjeu:
            ajouter_enjeu(numero_enjeu, description_enjeu, materialite)
            st.success(f"✅ Enjeu #{numero_enjeu} ajouté avec succès !")


# ------------------ 🔹 Mode : Gérer les Relations ------------------
elif mode_selection == "Gérer les Relations":
    st.sidebar.markdown("🔗 **Gérer les Relations**")
    relation_action = st.sidebar.radio("📌 Sélectionnez une Relation :", ["Associer un Maillon à une Catégorie"])

    if relation_action == "Associer un Maillon à une Catégorie":
        st.header("🔗 Associer un Maillon à une Catégorie")

        maillons_dict = get_maillons()
        categories_dict = get_categories()

        if maillons_dict and categories_dict:
            selected_maillon = st.selectbox("📌 Sélectionnez un Maillon :", list(maillons_dict.keys()))
            selected_categorie = st.selectbox("📌 Sélectionnez une Catégorie :", list(categories_dict.keys()))

            if st.button("✅ Associer", key="associer_maillon_categorie"):
                associer_maillon_categorie(maillons_dict[selected_maillon], categories_dict[selected_categorie])
                st.success(f"✅ '{selected_maillon}' a été associé à '{selected_categorie}' avec succès !")
        else:
            st.warning("⚠️ Aucun Maillon ou Catégorie disponible. Ajoutez des données d'abord !")




import sqlite3
import streamlit as st

# 🏆 Configurer la page
st.set_page_config(page_title="Dashboard ESG - Orange", page_icon="📊", layout="wide")

# 📌 Connexion à la base de données
def get_connection():
    return sqlite3.connect("database.db")

# 📌 Dictionnaire de correspondance entre entités et noms des tables SQL
entity_mapping = {
    "Maillon": "maillons",
    "Catégorie": "categories_parties_prenantes",
    "IRO": "iros",
    "Plan d'action": "plans_actions",
    "Enjeu": "enjeux"
}

# 📌 Sélection de l'entité à modifier
entity_type = st.selectbox("Choisissez une entité à modifier :", list(entity_mapping.keys()))

# Vérifier si l'entité existe bien
if entity_type in entity_mapping:
    table_name = entity_mapping[entity_type]

    # 📌 Récupération des éléments existants
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"SELECT id, nom FROM {table_name}")
        options = cursor.fetchall()
    except sqlite3.OperationalError:
        st.error(f"⚠️ La table `{table_name}` n'existe pas dans la base de données.")
        options = []

    conn.close()

    # 📌 Affichage des données et options de modification
    if options:
        st.subheader(f"📋 {entity_type}s existants :")

        for row in options:
            col1, col2, col3 = st.columns([3, 1, 1])
            col1.text(row[1])  # Nom de l'élément
            
            # Bouton Modifier
            if col2.button(f"Modifier {row[0]}", key=f"mod_{row[0]}"):
                selected_id = row[0]
                new_value = st.text_input("Nouvelle valeur :", row[1], key=f"new_val_{row[0]}")
                if st.button("Sauvegarder", key=f"save_{row[0]}"):
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET nom = ? WHERE id = ?", (new_value, selected_id))
                    conn.commit()
                    conn.close()
                    st.success("✅ Mise à jour effectuée !")
                    st.rerun()

            # Bouton Supprimer
            if col3.button(f"❌", key=f"del_{row[0]}"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row[0],))
                conn.commit()
                conn.close()
                st.warning("🚨 Élément supprimé !")
                st.rerun()
    else:
        st.info(f"Aucune donnée trouvée dans `{table_name}`.")
else:
    st.error("⚠️ Veuillez sélectionner une entité valide.")
