
import sys
from PyQt5.QtWidgets import QApplication
from database import DatabaseManager
from views.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    window = MainWindow(db_manager)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
