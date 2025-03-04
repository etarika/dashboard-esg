import sqlite3

# Connexion à la base SQLite
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# 🔹 Création des tables
cursor.executescript('''
CREATE TABLE IF NOT EXISTS categories_parties_prenantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS maillons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS iros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER UNIQUE NOT NULL,
    description TEXT,
    type TEXT,
    type_materialite TEXT
);

CREATE TABLE IF NOT EXISTS plans_actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER UNIQUE NOT NULL,
    type TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS enjeux (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER UNIQUE NOT NULL,
    description TEXT,
    materialite TEXT
);

-- Tables de relations
CREATE TABLE IF NOT EXISTS maillons_categories (
    maillon_id INTEGER,
    categorie_id INTEGER,
    FOREIGN KEY (maillon_id) REFERENCES maillons(id),
    FOREIGN KEY (categorie_id) REFERENCES categories_parties_prenantes(id),
    PRIMARY KEY (maillon_id, categorie_id)
);

CREATE TABLE IF NOT EXISTS maillons_iros (
    maillon_id INTEGER,
    iro_id INTEGER,
    FOREIGN KEY (maillon_id) REFERENCES maillons(id),
    FOREIGN KEY (iro_id) REFERENCES iros(id),
    PRIMARY KEY (maillon_id, iro_id)
);

CREATE TABLE IF NOT EXISTS maillons_enjeux (
    maillon_id INTEGER,
    enjeu_id INTEGER,
    FOREIGN KEY (maillon_id) REFERENCES maillons(id),
    FOREIGN KEY (enjeu_id) REFERENCES enjeux(id),
    PRIMARY KEY (maillon_id, enjeu_id)
);

CREATE TABLE IF NOT EXISTS maillons_plans_actions (
    maillon_id INTEGER,
    plan_id INTEGER,
    FOREIGN KEY (maillon_id) REFERENCES maillons(id),
    FOREIGN KEY (plan_id) REFERENCES plans_actions(id),
    PRIMARY KEY (maillon_id, plan_id)
);
''')

# Valider et fermer la connexion
conn.commit()
conn.close()

print("✅ Base de données initialisée avec succès !")
