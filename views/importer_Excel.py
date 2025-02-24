from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QFileDialog
import pandas as pd


class ImportTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.btn_import = QPushButton("Importer données depuis Excel")
        self.btn_import.clicked.connect(self.importer_excel)
        layout.addWidget(self.btn_import)
        self.setLayout(layout)

    def importer_excel(self):
        chemin, _ = QFileDialog.getOpenFileName(self, "Sélectionner le fichier Excel", "", "Excel Files (*.xlsx *.xls)")
        if not chemin:
            return
        try:
            df = pd.read_excel(chemin)
            for index, row in df.iterrows():
                candidat_data = {
                    'Numero_Table': int(row['Numero_Table']),
                    'Prenom': row['Prenom'],
                    'Nom': row['Nom'],
                    'Date_Naissance': row['Date_Naissance'].strftime("%Y-%m-%d") if not pd.isnull(row['Date_Naissance']) else "",
                    'Lieu_Naissance': row['Lieu_Naissance'],
                    'Sexe': row['Sexe'],
                    'Nationnalite': row['Nationnalite'],
                    'Choix_Epr_Facultative': bool(row['Choix_Epr_Facultative']),
                    'Epreuve_Facultative': row['Epreuve_Facultative'] if bool(row['Choix_Epr_Facultative']) else None,
                    'Aptitude_Sportive': bool(row['Aptitude_Sportive'])
                }
                self.db_manager.add_candidat(candidat_data)
            QMessageBox.information(self, "Succès", "Données importées avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'importation : {e}")