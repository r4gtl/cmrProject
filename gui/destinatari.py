import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from utils import center
from gui.addDestinatario import CrudDestinatario
from db.models import SessionLocal, Destinatario



class ViewDestinatari(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager - Elenco Destinatari")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1000,750)
        self.setFixedSize(self.size())
        self.crud_destinatario = CrudDestinatario()
        self.crud_destinatario.aboutToClose.connect(self.load_data)
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

        self.btnAddDestinatario = QPushButton("Aggiungi Destinatario")
        self.btnAddDestinatario.setIcon(QIcon('icons/addmember.png'))
        self.btnAddDestinatario.clicked.connect(self.openAddDestinatarioWindow)

        self.btnEditDestinatario = QPushButton("Aggiungi Destinatario")
        self.btnEditDestinatario.setIcon(QIcon('icons/addmember.png'))
        self.btnEditDestinatario.clicked.connect(self.openEditDestinatarioWindow)

        self.destinatariTable = QTableWidget(self)
        self.destinatariTable.setColumnCount(4)
        self.destinatariTable.setColumnHidden(0,True)
        self.destinatariTable.setHorizontalHeaderLabels(["ID", "Ragione Sociale", "Indirizzo_1", "Indirizzo_2"])
        header = self.destinatariTable.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.entrySearchLabel = QLabel("Cerca Destinatario")
        self.entrySearch = QLineEdit()
        self.entrySearch.textChanged.connect(self.search_destinatari)

        self.destinatariTable.cellDoubleClicked.connect(self.table_double_click)


    def layouts(self):
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.topLayout.addWidget(self.entrySearchLabel)
        self.topLayout.addWidget(self.entrySearch)
        self.topLayout.addWidget(self.btnAddDestinatario)
        self.topLayout.addWidget(self.btnExit)
        self.bottomLayout.addWidget(self.destinatariTable)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def load_data(self):
        self.destinatariTable.setRowCount(0)
        destinatari = self.session.query(Destinatario).all()
        for destinatario in destinatari:
            self.add_row(destinatario)
        self.destinatariTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def add_row(self, destinatario):
        row_position = self.destinatariTable.rowCount()
        self.destinatariTable.insertRow(row_position)
        self.destinatariTable.setItem(row_position, 0, QTableWidgetItem(str(destinatario.id)))
        self.destinatariTable.setItem(row_position, 1, QTableWidgetItem(destinatario.ragione_sociale))
        self.destinatariTable.setItem(row_position, 2, QTableWidgetItem(destinatario.indirizzo_1))
        self.destinatariTable.setItem(row_position, 3, QTableWidgetItem(destinatario.indirizzo_2))

    def search_destinatari(self):
        search_text = self.entrySearch.text()
        destinatari = self.session.query(Destinatario).filter(
            Destinatario.ragione_sociale.like(f'%{search_text}%')).all()
        self.destinatariTable.setRowCount(0)
        for destinatario in destinatari:
            self.add_row(destinatario)

    def table_double_click(self, row, column):
        item_id = self.destinatariTable.item(row, 0)
        if item_id:
            destinatario_id = int(item_id.text())
            destinatario = self.session.query(Destinatario).filter_by(id=destinatario_id).first()
            if destinatario:
                self.crud_destinatario.load_data(destinatario)
                self.crud_destinatario.show()


    def openAddDestinatarioWindow(self):
        self.crud_destinatario.show()

    def openEditDestinatarioWindow(self):
        pass