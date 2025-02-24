from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QComboBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


class JuryTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.layout = QFormLayout()

        # Liste déroulante pour sélectionner un jury existant
        self.combo_jury = QComboBox()
        self.combo_jury.currentIndexChanged.connect(self.load_selected_jury)
        self.layout.addRow("Jury :", self.combo_jury)


        self.input_region = QLineEdit()
        self.input_region.setPlaceholderText("Ex: Dakar")
        self.input_departement = QLineEdit()
        self.input_departement.setPlaceholderText("Ex: Dakar Centre")
        self.input_localite = QLineEdit()
        self.input_localite.setPlaceholderText("Ex: Plateau")
        self.input_centre = QLineEdit()
        self.input_centre.setPlaceholderText("Ex: Centre d'examen 1")
        self.input_president = QLineEdit()
        self.input_president.setPlaceholderText("Ex: M. Diouf")
        self.input_telephone = QLineEdit()
        self.input_telephone.setPlaceholderText("Ex: 771234567")

        # Validation du téléphone (uniquement des chiffres, 8 à 15 caractères)
        reg_ex = QRegExp("^[0-9]{8,15}$")
        telephone_validator = QRegExpValidator(reg_ex, self.input_telephone)
        self.input_telephone.setValidator(telephone_validator)

        self.layout.addRow("Région :", self.input_region)
        self.layout.addRow("Département :", self.input_departement)
        self.layout.addRow("Localité :", self.input_localite)
        self.layout.addRow("Centre d'Examen :", self.input_centre)
        self.layout.addRow("Président du Jury :", self.input_president)
        self.layout.addRow("Téléphone :", self.input_telephone)


        btn_layout = QHBoxLayout()
        self.btn_enregistrer = QPushButton("Ajouter Jury")
        self.btn_enregistrer.clicked.connect(self.save_jury)
        btn_layout.addWidget(self.btn_enregistrer)

        self.btn_update = QPushButton("Modifier Jury")
        self.btn_update.clicked.connect(self.update_jury)
        btn_layout.addWidget(self.btn_update)

        self.btn_delete = QPushButton("Supprimer Jury")
        self.btn_delete.clicked.connect(self.delete_jury)
        btn_layout.addWidget(self.btn_delete)


        self.btn_clear = QPushButton("Effacer")
        self.btn_clear.clicked.connect(self.clear_fields)
        btn_layout.addWidget(self.btn_clear)

        self.layout.addRow(btn_layout)
        self.setLayout(self.layout)


        self.load_jurys()

    def load_jurys(self):
        """Charge tous les jurys et met à jour la liste déroulante"""
        self.combo_jury.clear()
        jurys = self.db_manager.get_all_jurys()
        for jury in jurys:
            self.combo_jury.addItem(f"Jury {jury[0]} - {jury[1]} ({jury[4]})", jury[0])

    def load_selected_jury(self):
        """Charge les informations du jury sélectionné et active les boutons Modifier/Supprimer"""
        jury_id = self.combo_jury.currentData()

        if jury_id:
            jurys = self.db_manager.get_all_jurys()
            for jury in jurys:
                if jury[0] == jury_id:
                    self.input_region.setText(jury[1])
                    self.input_departement.setText(jury[2])
                    self.input_localite.setText(jury[3])
                    self.input_centre.setText(jury[4])
                    self.input_president.setText(jury[5])
                    self.input_telephone.setText(jury[6])


                    self.btn_update.setEnabled(True)
                    self.btn_delete.setEnabled(True)


                    self.btn_enregistrer.setText("Ajouter Nouveau Jury")
                    return

        # Si aucun jury n'est sélectionné, désactiver les boutons
        self.btn_update.setEnabled(False)
        self.btn_delete.setEnabled(False)

    def save_jury(self):
        """Ajoute un jury et affiche un message si un champ est vide"""
        try:

            jury_data = {
                "Region": self.input_region.text().strip(),
                "Departement": self.input_departement.text().strip(),
                "Localite": self.input_localite.text().strip(),
                "Centre_Examen": self.input_centre.text().strip(),
                "President_Jury": self.input_president.text().strip(),
                "Telephone": self.input_telephone.text().strip()
            }

            #  Vérifier que tous les champs sont remplis
            for key, value in jury_data.items():
                if not value:
                    QMessageBox.warning(self, "Erreur", f"Le champ '{key}' est obligatoire.")
                    return  # Arrête la fonction si un champ est vide

            #  Vérifier si un jury identique existe déjà
            if self.db_manager.jury_exists(jury_data):
                QMessageBox.warning(self, "Erreur", "Ce jury existe déjà !")
                return


            if self.db_manager.add_jury(jury_data):
                QMessageBox.information(self, "Succès", "Jury ajouté avec succès.")
                self.load_jurys()
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'ajouter le jury.")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {str(e)}")

    def update_jury(self):
        """Modifie un jury existant"""
        jury_id = self.combo_jury.currentData()
        if jury_id:
            jury_data = {
                "Region": self.input_region.text(),
                "Departement": self.input_departement.text(),
                "Localite": self.input_localite.text(),
                "Centre_Examen": self.input_centre.text(),
                "President_Jury": self.input_president.text(),
                "Telephone": self.input_telephone.text()
            }
            self.db_manager.update_jury(jury_id, jury_data)
            QMessageBox.information(self, "Succès", "Jury mis à jour.")
            self.load_jurys()

    def delete_jury(self):
        """Supprime un jury existant"""
        jury_id = self.combo_jury.currentData()
        if jury_id:
            self.db_manager.delete_jury(jury_id)
            QMessageBox.information(self, "Supprimé", "Le jury a été supprimé.")
            self.load_jurys()

    def clear_fields(self):
        """Réinitialise tous les champs et permet d'ajouter un nouveau jury."""
        self.input_region.clear()
        self.input_departement.clear()
        self.input_localite.clear()
        self.input_centre.clear()
        self.input_president.clear()
        self.input_telephone.clear()


        self.combo_jury.setCurrentIndex(-1)

        self.btn_enregistrer.setText("Ajouter Jury")

        self.btn_update.setEnabled(False)

        self.btn_delete.setEnabled(False)
