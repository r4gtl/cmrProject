import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from gui.cmr import AddCmr
from gui.cmr import AddCmr
from gui.destinatari import ViewDestinatari
from gui.destinazioni import ViewDestinazioni
from gui.trasportatori import ViewTrasportatori

from db.models import SessionLocal, Cmr

from utils import center




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)
        self.setFixedSize(self.size())
        self.add_cmr = AddCmr()
        self.view_destinatari = ViewDestinatari()
        self.view_destinazioni = ViewDestinazioni()
        self.view_trasportatori = ViewTrasportatori()
        self.session = SessionLocal()

        center(self)
        self.UI()
        self.show()


    def UI(self):
        self.toolBar()
        self.widgets()
        self.layouts()
        self.load_data()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        # ToolBar Buttons
        # New CMR
        self.addCMR = QAction(QIcon('icons/add.png'), "Nuovo Cmr", self)
        self.tb.addAction(self.addCMR)
        self.addCMR.triggered.connect(self.openAddCmrWindow)
        self.tb.addSeparator()
        self.addDestinatario = QAction(QIcon('icons/addmember.png'), "Destinatari", self)
        self.addDestinatario.triggered.connect(self.openViewDestinatarioWindow)
        self.tb.addAction(self.addDestinatario)
        # self.addDestinatario.triggered.connect(self.funcaddDestinatario)
        self.tb.addSeparator()
        self.addDestinazione = QAction(QIcon('icons/destination.png'), "Nuova Destinazione", self)
        self.tb.addAction(self.addDestinazione)
        self.addDestinazione.triggered.connect(self.openViewDestinazioneWindow)
        self.tb.addSeparator()
        self.addTrasportatore = QAction(QIcon('icons/delivery-truck.png'), "Nuovo Trasportatore", self)
        self.tb.addAction(self.addTrasportatore)
        self.addTrasportatore.triggered.connect(self.openViewTrasportatoreWindow)
        self.tb.addSeparator()




    def widgets(self):
            self.cmrTable = QTableWidget(self)
            self.cmrTable.setColumnCount(4)
            self.cmrTable.setColumnHidden(0, True)
            self.cmrTable.setHorizontalHeaderLabels(["ID", "Ragione Sociale", "Indirizzo_1", "Indirizzo_2"])
            header = self.cmrTable.horizontalHeader()
            header.setStretchLastSection(True)
            header.setSectionResizeMode(QHeaderView.Stretch)
            self.cmrTable.cellDoubleClicked.connect(self.table_double_click)

    def layouts(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.mainLayout = QVBoxLayout(central_widget)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.cmrTable)

        self.mainLayout.addLayout(self.bottomLayout)


    def openAddCmrWindow(self):
        self.add_cmr.show()

    def openViewDestinatarioWindow(self):
        self.view_destinatari.show()

    def openViewDestinazioneWindow(self):
        self.view_destinazioni.show()

    def openViewTrasportatoreWindow(self):
        self.view_trasportatori.show()

    def table_double_click(self, row, column):
        item_id = self.cmrTable.item(row, 0)
        if item_id:
            cmr_id = int(item_id.text())
            cmr = self.session.query(Cmr).filter_by(id=cmr_id).first()
            if cmr:
                self.add_cmr.load_data(cmr)
                self.add_cmr.show()


    def load_data(self):
        self.cmrTable.setRowCount(0)
        cmrs = self.session.query(Cmr).all()
        for cmr in cmrs:
            self.add_row(cmr)
        self.cmrTable.setEditTriggers(QAbstractItemView.NoEditTriggers)



