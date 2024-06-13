import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from gui.cmr import AddCmr
from gui.cmr import AddCmr
from gui.addDestinatario import AddDestinatario
from utils import center




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.add_cmr = AddCmr()
        self.add_destinatario = AddDestinatario()
        center(self)
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
        self.addCMR.triggered.connect(self.openAddCmrWindow)
        self.tb.addSeparator()
        self.addDestinatario = QAction(QIcon('icons/addmember.png'), "Nuovo Destinatario", self)
        self.addDestinatario.triggered.connect(self.openaddDestinatarioWindow)
        self.tb.addAction(self.addDestinatario)
        # self.addDestinatario.triggered.connect(self.funcaddDestinatario)
        self.tb.addSeparator()
        self.addDestinazione = QAction(QIcon('icons/destination.png'), "Nuova Destinazione", self)
        self.tb.addAction(self.addDestinazione)
        # self.addDestinazione.triggered.connect(self.funcaddDestinazione)
        self.tb.addSeparator()
        self.addTrasportatore = QAction(QIcon('icons/delivery-truck.png'), "Nuovo Trasportatore", self)
        self.tb.addAction(self.addTrasportatore)
        # self.addTrasportatore.triggered.connect(self.funcaddTrasportatore)
        self.tb.addSeparator()

    def openAddCmrWindow(self):
        self.add_cmr.show()

    def openaddDestinatarioWindow(self):
        self.add_destinatario.show()
