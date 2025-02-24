from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox,
    QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox )


class CandidateTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Formulaire de saisie des informations du candidat

        form_layout = QFormLayout()
        self.input_numero = QLineEdit()
        self.input_prenom = QLineEdit()
        self.input_nom = QLineEdit()
        self.input_date = QLineEdit()
        self.input_lieu = QLineEdit()

        # pour le sexe
        self.input_sexe = QComboBox()
        self.input_sexe.addItems(["M", "F"])

        self.input_nationalite = QLineEdit()

        # pour le Choix Epreuve Facultative
        self.input_choix = QComboBox()
        self.input_choix.addItems(["Oui", "Non"])

        self.input_epreuve = QLineEdit()

        # pour l'Aptitude Sportive
        self.input_aptitude = QComboBox()
        self.input_aptitude.addItems(["Apte", "Inapte"])

        form_layout.addRow("Numero Table :", self.input_numero)
        form_layout.addRow("Prenom :", self.input_prenom)
        form_layout.addRow("Nom :", self.input_nom)
        form_layout.addRow("Date de Naissance (YYYY-MM-DD) :", self.input_date)
        form_layout.addRow("Lieu de Naissance :", self.input_lieu)
        form_layout.addRow("Sexe (M/F) :", self.input_sexe)
        form_layout.addRow("Nationalite :", self.input_nationalite)
        form_layout.addRow("Choix Epreuve Facultative :", self.input_choix)
        form_layout.addRow("Epreuve Facultative :", self.input_epreuve)
        form_layout.addRow("Aptitude Sportive :", self.input_aptitude)
        main_layout.addLayout(form_layout)

        #  CRUD
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self.add_candidate)
        btn_layout.addWidget(self.btn_add)

        self.btn_update = QPushButton("Modifier")
        self.btn_update.clicked.connect(self.update_candidate)
        btn_layout.addWidget(self.btn_update)

        self.btn_delete = QPushButton("Supprimer")
        self.btn_delete.clicked.connect(self.delete_candidate)
        btn_layout.addWidget(self.btn_delete)

        self.btn_clear = QPushButton("Effacer")
        self.btn_clear.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.btn_clear)

        main_layout.addLayout(btn_layout)

        # afficher la liste des candidats
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Numero_Table", "Prenom", "Nom", "Date_Naissance", "Lieu_Naissance",
            "Sexe", "Nationalite", "Choix_Epr_Facultative", "Epreuve_Facultative", "Aptitude_Sportive"
        ])
        self.table.cellClicked.connect(self.table_item_clicked)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.load_candidates()

    def add_candidate(self):
        try:
            numero = int(self.input_numero.text())
        except Exception:
            QMessageBox.warning(self, "Erreur", "Numero Table doit être un entier.")
            return

        candidat_data = {
            "Numero_Table": numero,
            "Prenom": self.input_prenom.text().strip(),
            "Nom": self.input_nom.text().strip(),
            "Date_Naissance": self.input_date.text().strip(),
            "Lieu_Naissance": self.input_lieu.text().strip(),
            "Sexe": self.input_sexe.currentText().strip(),
            "Nationnalite": self.input_nationalite.text().strip(),
            "Choix_Epr_Facultative": True if self.input_choix.currentText().strip().lower() == "oui" else False,
            "Epreuve_Facultative": self.input_epreuve.text().strip(),
            "Aptitude_Sportive": True if self.input_aptitude.currentText().strip().lower() == "apte" else False,
        }
        # Vérification du candidat s'il a le même Numero_Table et Date_Naissance
        if self.db_manager.candidate_exists(candidat_data):
            QMessageBox.warning(
                self,
                "Erreur",
                "Ce candidat existe déjà (Numero Table et Date de Naissance déjà utilisés)."
            )
            return
        try:
            self.db_manager.add_candidat(candidat_data)
            QMessageBox.information(self, "Succès", "Candidat ajouté avec succès.")
            self.load_candidates()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def load_candidates(self):
        """Charge tous les candidats depuis la base et met à jour le tableau."""
        candidates = self.db_manager.get_all_candidates()
        self.table.setRowCount(0)

        for row_data in candidates:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for column, data in enumerate(row_data):
                self.table.setItem(row, column, QTableWidgetItem(str(data)))



    def table_item_clicked(self, row, column):
        """Lorsque l'utilisateur clique sur une ligne du tableau, charge les données dans le formulaire."""
        self.input_numero.setText(self.table.item(row, 0).text())
        self.input_prenom.setText(self.table.item(row, 1).text())
        self.input_nom.setText(self.table.item(row, 2).text())
        self.input_date.setText(self.table.item(row, 3).text())
        self.input_lieu.setText(self.table.item(row, 4).text())

        # mise a jour du sexe
        current_sexe = self.table.item(row, 5).text()
        index = self.input_sexe.findText(current_sexe)
        self.input_sexe.setCurrentIndex(index if index >= 0 else 0)

        self.input_nationalite.setText(self.table.item(row, 6).text())

        current_choix = self.table.item(row, 7).text()
        index = self.input_choix.findText("Oui" if current_choix in ["1", "True"] else "Non")
        self.input_choix.setCurrentIndex(index if index >= 0 else 0)

        self.input_epreuve.setText(self.table.item(row, 8).text())

        current_aptitude = self.table.item(row, 9).text()
        index = self.input_aptitude.findText("Apte" if current_aptitude in ["1", "True"] else "Inapte")
        self.input_aptitude.setCurrentIndex(index if index >= 0 else 0)

    def update_candidate(self):
        try:
            numero = int(self.input_numero.text())
        except Exception:
            QMessageBox.warning(self, "Erreur", "Numero Table doit être un entier.")
            return

        candidat_data = {
            "Numero_Table": numero,
            "Prenom": self.input_prenom.text().strip(),
            "Nom": self.input_nom.text().strip(),
            "Date_Naissance": self.input_date.text().strip(),
            "Lieu_Naissance": self.input_lieu.text().strip(),
            "Sexe": self.input_sexe.currentText().strip(),
            "Nationnalite": self.input_nationalite.text().strip(),
            "Choix_Epr_Facultative": True if self.input_choix.currentText().strip().lower() == "oui" else False,
            "Epreuve_Facultative": self.input_epreuve.text().strip(),
            "Aptitude_Sportive": True if self.input_aptitude.currentText().strip().lower() == "apte" else False,
        }
        try:
            if self.db_manager.update_candidat(numero, candidat_data):
                QMessageBox.information(self, "Succès", "Candidat modifié avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Candidat non trouvé pour modification.")
            self.load_candidates()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def delete_candidate(self):
        try:
            numero = int(self.input_numero.text())
        except Exception:
            QMessageBox.warning(self, "Erreur", "Numero Table doit être un entier.")
            return
        try:
            if self.db_manager.delete_candidat(numero):
                QMessageBox.information(self, "Succès", "Candidat supprimé avec succès.")
            else:
                QMessageBox.warning(self, "Erreur", "Candidat non trouvé pour suppression.")
            self.load_candidates()
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def clear_fields(self):
        self.input_numero.clear()
        self.input_prenom.clear()
        self.input_nom.clear()
        self.input_date.clear()
        self.input_lieu.clear()
        self.input_sexe.setCurrentIndex(0)
        self.input_nationalite.clear()
        self.input_choix.setCurrentIndex(0)
        self.input_epreuve.clear()
        self.input_aptitude.setCurrentIndex(0)
