from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox,
    QVBoxLayout, QTableWidget, QTableWidgetItem
)
from utils.anonymat import generer_anonymat
from controllers import calcul_bonus_malus_EPS


class NotesTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.input_numero = QLineEdit()
        form_layout.addRow("Numéro de Table :", self.input_numero)

        self.input_compo = QLineEdit()
        form_layout.addRow("Composition Française :", self.input_compo)
        self.input_dictee = QLineEdit()
        form_layout.addRow("Dictée :", self.input_dictee)
        self.input_etudeTexte = QLineEdit()
        form_layout.addRow("Etude de texte :", self.input_etudeTexte)
        self.input_InsCivique = QLineEdit()
        form_layout.addRow("Instruction civique :", self.input_InsCivique)
        self.input_histeGeo = QLineEdit()
        form_layout.addRow("Histoire, Géographie :", self.input_histeGeo)
        self.input_Math = QLineEdit()
        form_layout.addRow("Mathématiques :", self.input_Math)
        self.input_PCLv2 = QLineEdit()
        form_layout.addRow("PC / LV2 :", self.input_PCLv2)
        self.input_SVT = QLineEdit()
        form_layout.addRow("SVT :", self.input_SVT)
        self.input_AngE = QLineEdit()
        form_layout.addRow("Anglais (Écrit) :", self.input_AngE)
        self.input_AngO = QLineEdit()
        form_layout.addRow("Anglais (Oral) :", self.input_AngO)
        self.input_eps = QLineEdit()
        form_layout.addRow("EPS :", self.input_eps)
        self.input_epFac = QLineEdit()
        form_layout.addRow("Epreuve Facultative :", self.input_epFac)


        self.btn_enregistrer = QPushButton("Enregistrer Notes")
        self.btn_enregistrer.clicked.connect(self.save_notes)
        form_layout.addRow(self.btn_enregistrer)

        main_layout.addLayout(form_layout)

        self.btn_afficher = QPushButton("Afficher les notes")
        self.btn_afficher.clicked.connect(self.load_notes)
        main_layout.addWidget(self.btn_afficher)

        self.table_notes = QTableWidget()

        self.table_notes.setColumnCount(24)
        self.table_notes.setHorizontalHeaderLabels([
            "id", "Numero_Table", "Anonymat", "Compo_Franc", "Coef1", "Dictee", "Coef2",
            "Etude_de_texte", "Coef3", "Instruction_Civique", "Coef4", "Histoire_Geographie",
            "Coef5", "Mathématiques", "Coef6", "PC_LV2", "Coef7", "SVT", "Coef8",
            "Anglais1", "Coef9", "Anglais_Oral", "Coef10", "EPS", "Epreuve_Facultative", "Total_Points"
        ])
        main_layout.addWidget(self.table_notes)

        self.setLayout(main_layout)

    def save_notes(self):
        try:
            numero_table = int(self.input_numero.text())
            total_points = self.calculer_total_notes()

            # Génération automatique de l'anonymat
            anonymat = generer_anonymat()


            eps = float(self.input_eps.text())
            bonus, malus = calcul_bonus_malus_EPS(eps)
            print(f"EPS = {eps} -> Bonus = {bonus}, Malus = {malus}")
            print(f"Total Points Calculé = {total_points}")


            notes_data = {
                'Numero_Table': numero_table,
                'Anonymat': anonymat,
                'Compo_Franc': float(self.input_compo.text()),
                'Coef1': 2,
                'Dictee': float(self.input_dictee.text()),
                'Coef2': 1,
                'Etude_de_texte': float(self.input_etudeTexte.text()),
                'Coef3': 1,
                'Instruction_Civique': float(self.input_InsCivique.text()),
                'Coef4': 1,
                'Histoire_Geographie': float(self.input_histeGeo.text()),
                'Coef5': 2,
                'Mathématiques': float(self.input_Math.text()),
                'Coef6': 4,
                'PC_LV2': float(self.input_PCLv2.text()),
                'Coef7': 2,
                'SVT': float(self.input_SVT.text()),
                'Coef8': 2,
                'Anglais1': float(self.input_AngE.text()),
                'Coef9': 2,
                'Anglais_Oral': float(self.input_AngO.text()),
                'Coef10': 1,
                'EPS': eps,
                'Epreuve_Facultative': float(self.input_epFac.text()),
                'Total_Points': total_points
            }

            self.db_manager.add_notes_premier_tour(notes_data)
            QMessageBox.information(self, "Succès", "Notes enregistrées.\nAnonymat généré : " + anonymat)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement : {e}")

    def calculer_total_notes(self):
        try:
            compo = float(self.input_compo.text())
            dictee = float(self.input_dictee.text())
            etudeTexte = float(self.input_etudeTexte.text())
            InsCivique = float(self.input_InsCivique.text())
            histeGeo = float(self.input_histeGeo.text())
            Math = float(self.input_Math.text())
            PCLv2 = float(self.input_PCLv2.text())
            SVT = float(self.input_SVT.text())
            AngE = float(self.input_AngE.text())
            AngO = float(self.input_AngO.text())
            eps = float(self.input_eps.text())
            epFac = float(self.input_epFac.text())
        except Exception as e:
            print("Erreur de conversion:", e)
            return 0

        bonus, malus = calcul_bonus_malus_EPS(eps)
        effective_eps = eps + bonus - malus
        effective_epFac = (epFac - 10) if epFac > 10 else 0

        total_points = (
                compo * 2 +
                dictee * 1 +
                etudeTexte * 1 +
                InsCivique * 1 +
                histeGeo * 2 +
                Math * 4 +
                PCLv2 * 2 +
                SVT * 2 +
                AngE * 2 +
                AngO * 1 +
                effective_eps * 1 +
                effective_epFac
        )
        print(f"Total Points Calculé = {total_points}")
        return total_points

    def load_notes(self):
        try:
            notes_list = self.db_manager.get_all_notes()
            self.table_notes.setRowCount(0)
            for note in notes_list:
                row = self.table_notes.rowCount()
                self.table_notes.insertRow(row)

                for col, value in enumerate(note):
                    self.table_notes.setItem(row, col, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage des notes : {e}")
