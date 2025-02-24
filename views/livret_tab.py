from PyQt5.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox


class LivretTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        self.input_numero = QLineEdit()
        layout.addRow("Numéro de Table :", self.input_numero)

        self.input_nombre = QLineEdit()
        layout.addRow("Nombre de tentatives :", self.input_nombre)

        self.input_moy6e = QLineEdit()
        layout.addRow("Moyenne 6e :", self.input_moy6e)
        self.input_moy5e = QLineEdit()
        layout.addRow("Moyenne 5e :", self.input_moy5e)
        self.input_moy4e = QLineEdit()
        layout.addRow("Moyenne 4e :", self.input_moy4e)
        self.input_moy3e = QLineEdit()
        layout.addRow("Moyenne 3e :", self.input_moy3e)
        self.input_moycycle = QLineEdit()
        layout.addRow("Moyenne Cycle :", self.input_moycycle)

        self.btn_enregistrer = QPushButton("Enregistrer Livret Scolaire")
        self.btn_enregistrer.clicked.connect(self.save_livret)
        layout.addRow(self.btn_enregistrer)

        self.setLayout(layout)

    def save_livret(self):
        try:
            numero = int(self.input_numero.text())
            nombre = int(self.input_nombre.text())
            moy6e = float(self.input_moy6e.text())
            moy5e = float(self.input_moy5e.text())
            moy4e = float(self.input_moy4e.text())
            moy3e = float(self.input_moy3e.text())
            moycycle = float(self.input_moycycle.text())

            livret_data = {
                "Numero_Table": numero,
                "Nombre_de_fois": nombre,
                "Moyenne_6e": moy6e,
                "Moyenne_5e": moy5e,
                "Moyenne_4e": moy4e,
                "Moyenne_3e": moy3e,
                "Moyenne_Cycle": moycycle
            }

            self.db_manager.add_livret_scolaire(livret_data)
            QMessageBox.information(self, "Succès", "Livret scolaire enregistré avec succès.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement du livret scolaire : {e}")
