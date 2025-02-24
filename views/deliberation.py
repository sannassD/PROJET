from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from controllers import deliberation

class DeliberationTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Entrez le Numéro de Table")
        form_layout.addRow("Numéro de Table :", self.input_numero)

        self.input_tour = QLineEdit()
        self.input_tour.setPlaceholderText("Entrez 1 pour 1er tour ou 2 pour 2nd tour")
        form_layout.addRow("Tour d'examen :", self.input_tour)

        layout.addLayout(form_layout)

        self.btn_calculer = QPushButton("Calculer Délibération")
        self.btn_calculer.clicked.connect(self.calculer_deliberation)
        layout.addWidget(self.btn_calculer)

        self.label_result = QLabel("Résultat de la délibération :")
        layout.addWidget(self.label_result)

        self.setLayout(layout)

    def calculer_deliberation(self):
        try:
            numero = int(self.input_numero.text())
            tour = int(self.input_tour.text())


            notes = self.db_manager.get_notes_by_numero(numero)
            if not notes:
                QMessageBox.warning(self, "Erreur", "Aucune note trouvée pour ce candidat.")
                return
            total_points = notes[-1] if notes[-1] is not None else 0


            moyenne_cycle = self.db_manager.get_moyenne_cycle(numero)


            result = deliberation(total_points, moyenne_cycle, nombre_de_tentatives=1, tour=tour)
            self.label_result.setText(f"Résultat de la délibération : {result}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du calcul de la délibération : {e}")
