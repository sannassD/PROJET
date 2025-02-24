from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class ReleveTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Numéro de Table")
        layout.addWidget(self.input_numero)
        self.btn_generer = QPushButton("Générer relevé de notes")
        self.btn_generer.clicked.connect(self.generer_releve)
        layout.addWidget(self.btn_generer)
        self.txt_info = QTextEdit()
        self.txt_info.setReadOnly(True)
        layout.addWidget(self.txt_info)
        self.setLayout(layout)

    def generer_releve(self):
        try:
            numero = int(self.input_numero.text())
            conn = self.db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NotesPremierTour WHERE Numero_Table = ?", (numero,))
            notes = cursor.fetchone()
            conn.close()
            if not notes:
                QMessageBox.warning(self, "Avertissement", "Aucune note trouvée pour ce candidat.")
                return
            filename = f"releve_{numero}.pdf"
            c = canvas.Canvas(filename, pagesize=A4)
            width, height = A4
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, height - 50, f"Relevé de notes - Candidat {numero}")
            c.setFont("Helvetica", 10)


            c.drawString(50, height - 80, f"Composition Française : {notes[2]}")
            c.drawString(50, height - 100, f"Dictée : {notes[4]}")
            c.drawString(50, height - 120, f"Etude de texte : {notes[6]}")
            c.drawString(50, height - 140, f"Instruction Civique : {notes[8]}")
            c.drawString(50, height - 160, f"Histoire, Geographie : {notes[10]}")
            c.drawString(50, height - 180, f"Mathématiques : {notes[12]}")
            c.drawString(50, height - 200, f"PC / LV2 : {notes[14]}")
            c.drawString(50, height - 220, f"SVT : {notes[16]}")
            c.drawString(50, height - 240, f"Anglais(Ecrit) : {notes[18]}")
            c.drawString(50, height - 260, f"Anglais(Oral) : {notes[20]}")
            c.drawString(50, height - 280, f"EPS : {notes[22]}")
            c.drawString(50, height - 300, f"Epreuves facultativives : {notes[23]}")
            c.save()
            self.txt_info.setPlainText(f"Relevé généré : {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur : {e}")

