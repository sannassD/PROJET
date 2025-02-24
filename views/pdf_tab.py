from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QMessageBox
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
        self.btn_pdf_candidats = QPushButton("Générer la liste des candidats")
        self.btn_pdf_candidats.clicked.connect(self.generer_pdf_candidats)
        layout.addWidget(self.btn_pdf_candidats)
        self.txt_info = QTextEdit()
        self.txt_info.setReadOnly(True)
        layout.addWidget(self.txt_info)
        self.setLayout(layout)

    def generer_pdf_candidats(self):
        try:

            conn = self.db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Candidat")
            candidats = cursor.fetchall()
            conn.close()


            headers = ["Numero_Table", "Prenom", "Nom", "Date_Naissance",
                       "Lieu_Naissance", "Sexe", "Nationnalite",
                       "Choix_Epr_Facultative", "Epreuve_Facultative", "Aptitude_Sportive"]


            styles = getSampleStyleSheet()
            header_style = styles["Heading4"]
            normal_style = styles["Normal"]
            normal_style.fontSize = 8


            data = [[Paragraph(h, header_style) for h in headers]]
            for candidat in candidats:
                ligne = [Paragraph(str(champ), normal_style) for champ in candidat]
                data.append(ligne)

            col_widths = [60, 80, 80, 70, 80, 40, 80, 80, 80, 60]

            # Création du document PDF
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
            self.txt_info.setPlainText(f"PDF généré : {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF : {e}")


