import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from utils import center
from gui.addTrasportatore import CrudTrasportatore
from db.models import SessionLocal, Trasportatore



class ViewTrasportatori(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager - Elenco Destinazioni")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1000,750)
        self.setFixedSize(self.size())
        self.crud_trasportatore = CrudTrasportatore()
        self.crud_trasportatore.aboutToClose.connect(self.load_data)
        self.session = SessionLocal()

        center(self)

        self.UI()




    def UI(self):
        self.widgets()
        self.layouts()
        self.load_data()



    def widgets(self):
        self.btnExit = QPushButton("Esci")
        self.btnExit.setIcon(QIcon('icons/exit.png'))
        self.btnExit.clicked.connect(self.close)

        self.btnAddTrasportatore = QPushButton("Aggiungi Trasportatore")
        self.btnAddTrasportatore.setIcon(QIcon('icons/addmember.png'))
        self.btnAddTrasportatore.clicked.connect(self.openAddTrasportatoreWindow)

        # self.btnEditTrasportatore = QPushButton("Modifica Destinazione")
        # self.btnEditTrasportatore.setIcon(QIcon('icons/addmember.png'))
        # self.btnEditTrasportatore.clicked.connect(self.openEditTrasportatoreWindow)

        self.trasportatoriTable = QTableWidget(self)
        self.trasportatoriTable.setColumnCount(4)
        self.trasportatoriTable.setColumnHidden(0,True)
        self.trasportatoriTable.setHorizontalHeaderLabels(["ID", "Ragione Sociale", "Indirizzo_1", "Indirizzo_2"])
        header = self.trasportatoriTable.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.entrySearchLabel = QLabel("Cerca Trasportatore")
        self.entrySearch = QLineEdit()
        self.entrySearch.textChanged.connect(self.search_trasportatori)

        self.trasportatoriTable.cellDoubleClicked.connect(self.table_double_click)


    def layouts(self):
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.topLayout.addWidget(self.entrySearchLabel)
        self.topLayout.addWidget(self.entrySearch)
        self.topLayout.addWidget(self.btnAddTrasportatore)
        self.topLayout.addWidget(self.btnExit)
        self.bottomLayout.addWidget(self.trasportatoriTable)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def load_data(self):
        self.trasportatoriTable.setRowCount(0)
        trasportatori = self.session.query(Trasportatore).all()
        for trasportatore in trasportatori:
            self.add_row(trasportatore)
        self.trasportatoriTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def add_row(self, trasportatore):
        row_position = self.trasportatoriTable.rowCount()
        self.trasportatoriTable.insertRow(row_position)
        self.trasportatoriTable.setItem(row_position, 0, QTableWidgetItem(str(trasportatore.id)))
        self.trasportatoriTable.setItem(row_position, 1, QTableWidgetItem(trasportatore.ragione_sociale))
        self.trasportatoriTable.setItem(row_position, 2, QTableWidgetItem(trasportatore.indirizzo_1))
        self.trasportatoriTable.setItem(row_position, 3, QTableWidgetItem(trasportatore.indirizzo_2))

    def search_trasportatori(self):
        search_text = self.entrySearch.text()
        trasportatori = self.session.query(Trasportatore).filter(
            Trasportatore.ragione_sociale.like(f'%{search_text}%')).all()
        self.trasportatoriTable.setRowCount(0)
        for trasportatore in trasportatori:
            self.add_row(trasportatore)

    def table_double_click(self, row, column):
        item_id = self.trasportatoriTable.item(row, 0)
        if item_id:
            trasportatore_id = int(item_id.text())
            trasportatore = self.session.query(Trasportatore).filter_by(id=trasportatore_id).first()
            if trasportatore:
                self.crud_trasportatore.load_data(trasportatore)
                self.crud_trasportatore.show()


    def openAddTrasportatoreWindow(self):
        self.crud_trasportatore.show()

    def openEditDestinazioneWindow(self):
        pass