from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox)
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from controllers import deliberation

class ReleveTab(QWidget):
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.sum_coefs = 18
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()


        self.input_numero = QLineEdit()
        self.input_numero.setPlaceholderText("Numéro de Table")
        layout.addWidget(self.input_numero)


        self.btn_afficher = QPushButton("Afficher relevé")
        self.btn_afficher.clicked.connect(self.afficher_releve)
        layout.addWidget(self.btn_afficher)


        self.txt_info = QTextEdit()
        self.txt_info.setReadOnly(True)
        layout.addWidget(self.txt_info)


        self.btn_generer = QPushButton("Générer PDF")
        self.btn_generer.clicked.connect(self.generer_pdf)
        layout.addWidget(self.btn_generer)

        self.setLayout(layout)

    # ====================== PARTIE AFFICHAGE ======================
    def afficher_releve(self):

        try:
            numero = int(self.input_numero.text())


            candidat_info = self._get_candidat_info(numero)
            if not candidat_info:
                QMessageBox.warning(self, "Avertissement", "Candidat introuvable.")
                return


            notes = self._get_notes_premier_tour(numero)
            if not notes:
                QMessageBox.warning(self, "Avertissement", "Aucune note trouvée pour ce candidat.")
                return


            total_points = notes[25]
            moyenne_bfem = round(total_points / self.sum_coefs, 2)
            resultat_delib = deliberation(total_points, moyenne_bfem, 1, 1)


            report = (
                "RÉPUBLIQUE ALGERIENNE DÉMOCRATIQUE ET POPULAIRE\n"
                "MINISTÈRE DE L'ÉDUCATION NATIONALE\n"
                "OFFICE NATIONAL DES EXAMENS ET CONCOURS\n\n"
                "RELEVÉ DE NOTES (Prévisualisation)\n\n"
            )
            report += f"Nom : {candidat_info['Nom']}\n"
            report += f"Prénom : {candidat_info['Prenom']}\n"
            report += f"Date de naissance : {candidat_info['Date_Naissance']} | Lieu : {candidat_info['Lieu_Naissance']}\n"
            report += f"Nombre de tentatives : {candidat_info['Nombre_de_fois']}\n"
            report += f"Numéro de Table : {numero}\n\n"

            report += f"Composition Française : {notes[3]} (Coef: {notes[4]})\n"
            report += f"Dictée : {notes[5]} (Coef: {notes[6]})\n"
            report += f"Etude de texte : {notes[7]} (Coef: {notes[8]})\n"
            report += f"Instruction Civique : {notes[9]} (Coef: {notes[10]})\n"
            report += f"Histoire, Géographie : {notes[11]} (Coef: {notes[12]})\n"
            report += f"Mathématiques : {notes[13]} (Coef: {notes[14]})\n"
            report += f"PC / LV2 : {notes[15]} (Coef: {notes[16]})\n"
            report += f"SVT : {notes[17]} (Coef: {notes[18]})\n"
            report += f"Anglais (Écrit) : {notes[19]} (Coef: {notes[20]})\n"
            report += f"Anglais (Oral) : {notes[21]} (Coef: {notes[22]})\n"
            report += f"EPS : {notes[23]}\n"
            report += f"Epreuve Facultative : {notes[24]}\n\n"
            report += f"Total des points : {total_points}\n"
            report += f"Moyenne BFEM : {moyenne_bfem}\n"
            report += f"Résultat de la délibération : {resultat_delib}\n"

            self.txt_info.setPlainText(report)

        except ValueError:
            QMessageBox.warning(self, "Avertissement", "Le numéro de table doit être un entier.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'affichage du relevé : {e}")

    # ====================== PARTIE GENERATION PDF ======================
    def generer_pdf(self):

        try:
            numero = int(self.input_numero.text())


            candidat_info = self._get_candidat_info(numero)
            if not candidat_info:
                QMessageBox.warning(self, "Avertissement", "Candidat introuvable.")
                return


            notes = self._get_notes_premier_tour(numero)
            if not notes:
                QMessageBox.warning(self, "Avertissement", "Aucune note trouvée pour ce candidat.")
                return

            total_points = notes[25]
            moyenne_bfem = round(total_points / self.sum_coefs, 2)
            resultat_delib = deliberation(total_points, moyenne_bfem, 1, 1)

            filename = f"releve_{numero}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            styles = getSampleStyleSheet()
            styleN = styles['Normal']


            entete_data = [
                ["RÉPUBLIQUE DU SENEGAL"],
                ["MINISTÈRE DE L'ÉDUCATION NATIONALE"],
                ["OFFICE NATIONAL DES EXAMENS ET CONCOURS"],
                [""],
                ["RELEVÉ DE NOTES"]
            ]
            entete_table = Table(entete_data, colWidths=[400])
            entete_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
            ]))


            decoration_data = [[""]]
            decoration_table = Table(decoration_data, colWidths=[400], rowHeights=[3])
            decoration_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ]))


            infos_data = [
                [Paragraph(f"Nom : <b>{candidat_info['Nom']}</b>", styleN)],
                [Paragraph(f"Prénom : <b>{candidat_info['Prenom']}</b>", styleN)],
                [Paragraph(f"Date de naissance : <b>{candidat_info['Date_Naissance']}</b>", styleN)],
                [Paragraph(f"Lieu de naissance : <b>{candidat_info['Lieu_Naissance']}</b>", styleN)],
                [Paragraph(f"Nombre de tentatives : <b>{candidat_info['Nombre_de_fois']}</b>", styleN)],
                [Paragraph(f"Numéro de Table : <b>{numero}</b>", styleN)]
            ]
            infos_table = Table(infos_data, colWidths=[400])
            infos_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ]))


            subjects_data = [
                ["Matière", "Note", "Coef"],
                ["Compo Française", notes[3], notes[4]],
                ["Dictée", notes[5], notes[6]],
                ["Etude de texte", notes[7], notes[8]],
                ["Instruction Civique", notes[9], notes[10]],
                ["Histoire, Géographie", notes[11], notes[12]],
                ["Mathématiques", notes[13], notes[14]],
                ["PC / LV2", notes[15], notes[16]],
                ["SVT", notes[17], notes[18]],
                ["Anglais (Écrit)", notes[19], notes[20]],
                ["Anglais (Oral)", notes[21], notes[22]],
                ["EPS", notes[23], "-"],
                ["Epreuve Facultative", notes[24], "-"],
            ]
            subjects_table = Table(subjects_data, colWidths=[150, 100, 50])
            subjects_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER')
            ]))


            final_data = [
                ["Total Points", str(total_points)],
                ["Moyenne ", str(moyenne_bfem)],
                ["Délibération", str(resultat_delib)]
            ]
            final_table = Table(final_data, colWidths=[200, 200])
            final_table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, 0), colors.lightgrey),
            ]))

            from reportlab.platypus import Spacer
            elements = []
            elements.append(entete_table)
            elements.append(Spacer(1, 10))
            elements.append(decoration_table)
            elements.append(Spacer(1, 20))
            elements.append(infos_table)
            elements.append(Spacer(1, 20))
            elements.append(subjects_table)
            elements.append(Spacer(1, 20))
            elements.append(final_table)

            doc.build(elements)
            QMessageBox.information(self, "Succès", f"PDF généré : {filename}")

        except ValueError:
            QMessageBox.warning(self, "Avertissement", "Le numéro de table doit être un entier.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la génération du PDF : {e}")


    def _get_candidat_info(self, numero_table):

        try:
            conn = self.db_manager.connect()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT Prenom, Nom, Date_Naissance, Lieu_Naissance
                FROM Candidat
                WHERE Numero_Table=?
            """, (numero_table,))
            row_candidat = cursor.fetchone()

            if not row_candidat:
                conn.close()
                return None

            prenom, nom, date_naiss, lieu_naiss = row_candidat


            cursor.execute("""
                SELECT Nombre_de_fois
                FROM LivretScolaire
                WHERE Numero_Table=?
            """, (numero_table,))
            row_livret = cursor.fetchone()
            conn.close()

            nombre_fois = row_livret[0] if row_livret else 1

            return {
                "Prenom": prenom,
                "Nom": nom,
                "Date_Naissance": date_naiss,
                "Lieu_Naissance": lieu_naiss,
                "Nombre_de_fois": nombre_fois
            }
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération du candidat : {e}")
            return None

    def _get_notes_premier_tour(self, numero_table):

        conn = self.db_manager.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NotesPremierTour WHERE Numero_Table = ?", (numero_table,))
        notes = cursor.fetchone()
        conn.close()
        return notes
