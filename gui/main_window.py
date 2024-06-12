import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def UI(self):
        self.toolBar()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ToolBar Buttons
        # New CMR
        self.addCMR = QAction(QIcon('icons/add.png'), "Nuovo Cmr", self)
        self.tb.addAction(self.addCMR)
        #self.addCMR.triggered.connect(self.funcaddCMR)
        self.tb.addSeparator()
