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

if categories:
    st.subheader("📋 Catégories existantes :")
    for id_cat, nom_cat in get_categories().items():
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.text(nom_cat)  # Nom de la catégorie
        
        # Modifier une catégorie
        if col2.button(f"Modifier {id_cat}", key=f"mod_cat_{id_cat}"):
            new_value = st.text_input("Nouvelle valeur :", nom_cat, key=f"new_val_cat_{id_cat}")
            if st.button("Sauvegarder", key=f"save_cat_{id_cat}"):
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE categories_parties_prenantes SET nom = ? WHERE id = ?", (new_value, id_cat))
                conn.commit()
                conn.close()
                st.success(f"✅ Catégorie '{nom_cat}' mise à jour avec succès !")
                st.rerun()

        # Supprimer une catégorie
        if col3.button(f"❌", key=f"del_cat_{id_cat}"):
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM categories_parties_prenantes WHERE id = ?", (id_cat,))
            conn.commit()
            conn.close()
            st.warning(f"🚨 Catégorie '{nom_cat}' supprimée !")
            st.rerun()

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

if maillons:
    st.subheader("📋 Maillons existants :")
    for id_maillon, nom_maillon in get_maillons().items():
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.text(nom_maillon)

        # Modifier un Maillon
        if col2.button(f"Modifier {id_maillon}", key=f"mod_mai_{id_maillon}"):
            new_value = st.text_input("Nouvelle valeur :", nom_maillon, key=f"new_val_mai_{id_maillon}")
            if st.button("Sauvegarder", key=f"save_mai_{id_maillon}"):
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE maillons SET nom = ? WHERE id = ?", (new_value, id_maillon))
                conn.commit()
                conn.close()
                st.success(f"✅ Maillon '{nom_maillon}' mis à jour avec succès !")
                st.rerun()

        # Supprimer un Maillon
        if col3.button(f"❌", key=f"del_mai_{id_maillon}"):
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM maillons WHERE id = ?", (id_maillon,))
            conn.commit()
            conn.close()
            st.warning(f"🚨 Maillon '{nom_maillon}' supprimé !")
            st.rerun()


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




