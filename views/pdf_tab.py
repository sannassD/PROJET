from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
)
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class PDFListsTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Bouton pour afficher la liste des candidats
        self.btn_afficher = QPushButton("Afficher la liste des candidats")
        self.btn_afficher.clicked.connect(self.load_candidates)
        layout.addWidget(self.btn_afficher)

        # Bouton pour générer le PDF
        self.btn_generate_pdf = QPushButton("Générer PDF")
        self.btn_generate_pdf.clicked.connect(self.generer_pdf_candidats)
        layout.addWidget(self.btn_generate_pdf)


        self.table_candidates = QTableWidget()
        self.table_candidates.setColumnCount(10)
        self.table_candidates.setHorizontalHeaderLabels([
            "Numero Table", "Prenom", "Nom", "Date Naissance",
            "Lieu Naissance", "Sexe", "Nationnalite",
            "Choix Epr Facultative", "Epreuve Facultative", "Aptitude Sportive"
        ])
        layout.addWidget(self.table_candidates)
        self.table_candidates.hide()

        self.setLayout(layout)

    def load_candidates(self):

        try:
            candidats = self.db_manager.get_all_candidates()
            self.table_candidates.setRowCount(0)
            for candidat in candidats:
                row = self.table_candidates.rowCount()
                self.table_candidates.insertRow(row)
                for col, value in enumerate(candidat):
                    self.table_candidates.setItem(row, col, QTableWidgetItem(str(value)))
            self.table_candidates.show()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage des candidats : {e}")

    def generer_pdf_candidats(self):
        try:
            candidats = self.db_manager.get_all_candidates()
            if not candidats:
                QMessageBox.warning(self, "Avertissement", "Aucun candidat à afficher.")
                return

            headers = [
                "Numero Table", "Prenom", "Nom", "Date Naissance",
                "Lieu Naissance", "Sexe", "Nationnalite",
                "Choix Epr Facultative", "Epreuve Facultative", "Aptitude Sportive"
            ]

            styles = getSampleStyleSheet()
            header_style = styles["Heading4"]
            normal_style = styles["Normal"]
            normal_style.fontSize = 8

            data = [[Paragraph(h, header_style) for h in headers]]
            for candidat in candidats:
                ligne_data = list(candidat)
                choix = ligne_data[7]
                if choix is None:
                    ligne_data[7] = "Non"
                elif str(choix).strip() in ["1", "True"]:
                    ligne_data[7] = "Oui"
                else:
                    ligne_data[7] = "Non"

                aptitude = ligne_data[9]
                try:
                    if int(aptitude) == 1:
                        ligne_data[9] = "Apte"
                    else:
                        ligne_data[9] = "Inapte"
                except Exception:
                    ligne_data[9] = str(aptitude)

                ligne = [Paragraph(str(champ), normal_style) for champ in ligne_data]
                data.append(ligne)

            col_widths = [50, 65, 65, 55, 65, 35, 70, 65, 65, 50]


            filename = "liste_candidats.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            tableau = Table(data, colWidths=col_widths)

            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            tableau.setStyle(style)

            doc.build([tableau])
            QMessageBox.information(self, "Succès", f"PDF généré : {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF : {e}")
