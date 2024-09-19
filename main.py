import sys
import os
from PyQt5.QtWidgets import QApplication



from gui.main_window import MainWindow

from db.database import init_db





def main():
    init_db()
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
