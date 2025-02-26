import sqlite3

class DatabaseManager:
    def __init__(self, db_name="bfem.db"):
        self.db_name = db_name
        self.create_database()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_database(self):
        conn = self.connect()
        cursor = conn.cursor()

        # Table Candidat
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Candidat (
                Numero_Table INTEGER PRIMARY KEY,
                Prenom TEXT,
                Nom TEXT,
                Date_Naissance TEXT,
                Lieu_Naissance TEXT,
                Sexe TEXT,
                Nationnalite TEXT,
                Choix_Epr_Facultative BOOLEAN,
                Epreuve_Facultative TEXT,
                Aptitude_Sportive BOOLEAN
            )
        ''')

        # Table LivretScolaire
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS LivretScolaire (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Numero_Table INTEGER,
                Nombre_de_fois INTEGER,
                Moyenne_6e REAL,
                Moyenne_5e REAL,
                Moyenne_4e REAL,
                Moyenne_3e REAL,
                Moyenne_Cycle REAL,
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')

        # Table NotesPremierTour
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS NotesPremierTour (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Numero_Table INTEGER,
                Anonymat TEXT,
                Compo_Franc REAL,
                Coef1 INTEGER,
                Dictee REAL,
                Coef2 INTEGER,
                Etude_de_texte REAL,
                Coef3 INTEGER,
                Instruction_Civique REAL,
                Coef4 INTEGER,
                Histoire_Geographie REAL,
                Coef5 INTEGER,
                Mathématiques REAL,
                Coef6 INTEGER,
                PC_LV2 REAL,
                Coef7 INTEGER,
                SVT REAL,
                Coef8 INTEGER,
                Anglais1 REAL,
                Coef9 INTEGER,
                Anglais_Oral REAL,
                Coef10 INTEGER,
                EPS REAL,
                Epreuve_Facultative REAL,
                Total_Points REAL,
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')

        # Table NotesSecondTour
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS NotesSecondTour (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Numero_Table INTEGER,
                Francais REAL,
                CoefA INTEGER,
                Mathématiques REAL,
                CoefB INTEGER,
                PC_LV2 REAL,
                CoefC INTEGER,
                Total_Points REAL,
                FOREIGN KEY (Numero_Table) REFERENCES Candidat(Numero_Table)
            )
        ''')

        # Table du Jury
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Jury (
                id_jury INTEGER PRIMARY KEY AUTOINCREMENT,
                Region TEXT NOT NULL,
                Departement TEXT NOT NULL,
                Localite TEXT NOT NULL,
                Centre_Examen TEXT NOT NULL,
                President_Jury TEXT NOT NULL,
                Telephone TEXT NOT NULL
            );

        ''')

        conn.commit()
        conn.close()

    def add_candidat(self, candidat_data):
        conn = self.connect()
        cursor = conn.cursor()
        query = '''
            INSERT INTO Candidat (Numero_Table, Prenom, Nom, Date_Naissance, Lieu_Naissance,
                                    Sexe, Nationnalite, Choix_Epr_Facultative, Epreuve_Facultative, Aptitude_Sportive)
            VALUES (:Numero_Table, :Prenom, :Nom, :Date_Naissance, :Lieu_Naissance,
                    :Sexe, :Nationnalite, :Choix_Epr_Facultative, :Epreuve_Facultative, :Aptitude_Sportive)
        '''
        cursor.execute(query, candidat_data)
        conn.commit()
        conn.close()

    def get_candidat(self, numero_table):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Candidat WHERE Numero_Table = ?", (numero_table,))
        candidat = cursor.fetchone()
        conn.close()
        return candidat

    def candidate_exists(self, candidat_data):
        """
        Vérifie si un candidat avec le même Numero_Table et Date_Naissance existe déjà.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Candidat WHERE Numero_Table=? AND Date_Naissance=?
        """, (candidat_data["Numero_Table"], candidat_data["Date_Naissance"]))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists


    def get_all_candidates(self):
        """Retourne la liste de tous les candidats enregistrés."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Candidat")
        candidates = cursor.fetchall()
        conn.close()
        return candidates

    def update_candidat(self, numero_table, candidat_data):
        """Met à jour un candidat existant identifié par Numero_Table."""
        conn = self.connect()
        cursor = conn.cursor()
        query = """
            UPDATE Candidat
            SET Prenom=?, Nom=?, Date_Naissance=?, Lieu_Naissance=?, Sexe=?, Nationnalite=?,
                Choix_Epr_Facultative=?, Epreuve_Facultative=?, Aptitude_Sportive=?
            WHERE Numero_Table=?
        """
        cursor.execute(query, (
            candidat_data["Prenom"],
            candidat_data["Nom"],
            candidat_data["Date_Naissance"],
            candidat_data["Lieu_Naissance"],
            candidat_data["Sexe"],
            candidat_data["Nationnalite"],
            1 if candidat_data["Choix_Epr_Facultative"] else 0,
            candidat_data["Epreuve_Facultative"],
            1 if candidat_data["Aptitude_Sportive"] else 0,
            numero_table
        ))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    def delete_candidat(self, numero_table):
        """Supprime le candidat identifié par Numero_Table."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Candidat WHERE Numero_Table=?", (numero_table,))
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        return affected > 0

    def add_livret_scolaire(self, livret_data):
        conn = self.connect()
        cursor = conn.cursor()
        query = '''
            INSERT INTO LivretScolaire 
            (Numero_Table, Nombre_de_fois, Moyenne_6e, Moyenne_5e, Moyenne_4e, Moyenne_3e, Moyenne_Cycle)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (
            livret_data["Numero_Table"],
            livret_data["Nombre_de_fois"],
            livret_data["Moyenne_6e"],
            livret_data["Moyenne_5e"],
            livret_data["Moyenne_4e"],
            livret_data["Moyenne_3e"],
            livret_data["Moyenne_Cycle"]
        ))
        conn.commit()
        conn.close()

    def get_moyenne_cycle(self, numero_table):
        """
        Récupère la moyenne du cycle pour le candidat identifié par numero_table.
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Moyenne_Cycle FROM LivretScolaire WHERE Numero_Table=?
        """, (numero_table,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def get_notes_by_numero(self, numero_table):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM NotesPremierTour WHERE Numero_Table=? ORDER BY id ASC LIMIT 1
        """, (numero_table,))
        result = cursor.fetchone()
        conn.close()
        return result

    def add_notes_premier_tour(self, notes_data):
        conn = self.connect()
        cursor = conn.cursor()
        query = '''
            INSERT INTO NotesPremierTour (
                Numero_Table, Compo_Franc, Coef1, Dictee, Coef2, Etude_de_texte, Coef3,
                Instruction_Civique, Coef4, Histoire_Geographie, Coef5, Mathématiques, Coef6,
                PC_LV2, Coef7, SVT, Coef8, Anglais1, Coef9, Anglais_Oral, Coef10, EPS, Epreuve_Facultative
            )
            VALUES (
                :Numero_Table, :Compo_Franc, :Coef1, :Dictee, :Coef2, :Etude_de_texte, :Coef3,
                :Instruction_Civique, :Coef4, :Histoire_Geographie, :Coef5, :Mathématiques, :Coef6,
                :PC_LV2, :Coef7, :SVT, :Coef8, :Anglais1, :Coef9, :Anglais_Oral, :Coef10, :EPS, :Epreuve_Facultative
            )
        '''
        cursor.execute(query, notes_data)
        conn.commit()
        conn.close()

    def get_all_notes(self):
            """Retourne la liste de toutes les notes enregistrées dans NotesPremierTour."""
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NotesPremierTour ORDER BY id ASC")
            results = cursor.fetchall()
            conn.close()
            return results



    def jury_exists(self, jury_data):
        """Vérifie si un jury avec les mêmes informations existe déjà dans la base."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
               SELECT * FROM Jury WHERE Region=? AND Departement=? AND Localite=? 
               AND Centre_Examen=? AND President_Jury=? AND Telephone=?
           """, (
            jury_data["Region"], jury_data["Departement"], jury_data["Localite"],
            jury_data["Centre_Examen"], jury_data["President_Jury"], jury_data["Telephone"]
        ))
        existing_jury = cursor.fetchone()
        conn.close()
        return existing_jury is not None


    def add_jury(self, jury_data):
        """Ajoute un nouveau jury si un jury identique n'existe pas déjà."""
        if self.jury_exists(jury_data):
            return False

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
               INSERT INTO Jury (Region, Departement, Localite, Centre_Examen, President_Jury, Telephone)
               VALUES (?, ?, ?, ?, ?, ?)
           """, (
            jury_data["Region"], jury_data["Departement"], jury_data["Localite"],
            jury_data["Centre_Examen"], jury_data["President_Jury"], jury_data["Telephone"]
        ))
        conn.commit()
        conn.close()
        return True



    def get_all_jurys(self):
        """Retourne la liste de tous les jurys enregistrés dans la base."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Jury ORDER BY id_jury ASC")
        jurys = cursor.fetchall()
        conn.close()
        return jurys



    def update_jury(self, jury_id, jury_data):
        """Met à jour un jury existant en base après vérification de son existence."""
        conn = self.connect()
        cursor = conn.cursor()

        # Vérifier si le jury existe avant de le modifier
        cursor.execute("SELECT * FROM Jury WHERE id_jury=?", (jury_id,))
        existing_jury = cursor.fetchone()
        if existing_jury is None:
            conn.close()
            return False

        cursor.execute("""
               UPDATE Jury SET Region=?, Departement=?, Localite=?, Centre_Examen=?, President_Jury=?, Telephone=?
               WHERE id_jury=?
           """, (
            jury_data["Region"], jury_data["Departement"], jury_data["Localite"],
            jury_data["Centre_Examen"], jury_data["President_Jury"], jury_data["Telephone"], jury_id
        ))
        conn.commit()
        conn.close()
        return True



    def delete_jury(self, jury_id):
        """Supprime un jury en fonction de son ID après vérification de son existence."""
        conn = self.connect()
        cursor = conn.cursor()

        # Vérifier si le jury existe avant suppression
        cursor.execute("SELECT * FROM Jury WHERE id_jury=?", (jury_id,))
        existing_jury = cursor.fetchone()
        if existing_jury is None:
            conn.close()
            return False

        cursor.execute("DELETE FROM Jury WHERE id_jury=?", (jury_id,))
        conn.commit()
        conn.close()
        return True