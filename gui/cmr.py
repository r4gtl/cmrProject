import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt



class AddCmr(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.UI()
        self.show()


    def UI(self):
        self.layouts()
        self.toolBar()

    def toolBar(self):
        self.tb = QToolBar("Tool Bar", self)
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.layout.addWidget(self.tb)  # Aggiunta della toolbar al layout
        self.layout.addStretch()  # Aggiunta di uno spacer per spingere il contenuto in basso

        # ToolBar Buttons
        # New CMR
        self.addSave = QAction(QIcon('icons/save.png'), "Salva", self)
        self.tb.addAction(self.addSave)
        # self.addSave.triggered.connect(self.funcaddSave)
        self.tb.addSeparator()
        self.deleteCmr = QAction(QIcon('icons/delete-folder.png'), "Elimina Cmr", self)
        self.tb.addAction(self.deleteCmr)
        # self.deleteCmr.triggered.connect(self.funcdeleteCmr)
        self.tb.addSeparator()
        self.exit = QAction(QIcon('icons/exit.png'), "Esci", self)
        self.tb.addAction(self.exit)
        # self.exit.triggered.connect(self.funcexit)
        self.tb.addSeparator()

    def layouts(self):
        self.layout = QVBoxLayout()  # Creazione del layout verticale
        self.setLayout(self.layout)  # Impostazione del layout per il widget

