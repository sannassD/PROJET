from PyQt5.QtWidgets import QMainWindow, QTabWidget
from controllers import deliberation
from views.jury_tab import JuryTab
from views.candidate_tab import CandidateTab
from views.notes_tab import NotesTab
from views.livret_tab import LivretTab
from views.pdf_tab import PDFListsTab
from views.releve_tab import ReleveTab
from views.importer_Excel import ImportTab
from views.deliberation import DeliberationTab

class MainWindow(QMainWindow):
    def __init__(self, db_manager):
        super().__init__()
        self.setWindowTitle("Application de Gestion BFEM")
        self.setGeometry(100, 100, 700, 600)
        self.db_manager = db_manager
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.addTab(JuryTab(self.db_manager), "Paramétrage Jury")
        self.tabs.addTab(CandidateTab(self.db_manager), "Gestion Candidats")
        self.tabs.addTab(NotesTab(self.db_manager), "Saisie des Notes")
        self.tabs.addTab(LivretTab(self.db_manager), "Livret Scolaire")
        self.tabs.addTab(PDFListsTab(self.db_manager), "Liste des Candidats")
        self.tabs.addTab(DeliberationTab(self.db_manager), "Délibération")
        self.tabs.addTab(ReleveTab(self.db_manager), "Relevé de notes")
        self.tabs.addTab(ImportTab(self.db_manager), "Importer Excel")
        self.setCentralWidget(self.tabs)
