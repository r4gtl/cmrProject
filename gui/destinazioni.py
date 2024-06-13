import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from utils import center
from gui.addDestinazione import CrudDestinazione
from db.models import SessionLocal, Destinazione



class ViewDestinazioni(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager - Elenco Destinazioni")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1000,750)
        self.setFixedSize(self.size())
        self.crud_destinazione = CrudDestinazione()
        self.crud_destinazione.aboutToClose.connect(self.load_data)
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

        self.btnAddDestinazione = QPushButton("Aggiungi Destinazione")
        self.btnAddDestinazione.setIcon(QIcon('icons/addmember.png'))
        self.btnAddDestinazione.clicked.connect(self.openAddDestinazioneWindow)

        self.btnEditDestinazione = QPushButton("Modifica Destinazione")
        self.btnEditDestinazione.setIcon(QIcon('icons/addmember.png'))
        self.btnEditDestinazione.clicked.connect(self.openEditDestinazioneWindow)

        self.destinazioniTable = QTableWidget(self)
        self.destinazioniTable.setColumnCount(4)
        self.destinazioniTable.setColumnHidden(0,True)
        self.destinazioniTable.setHorizontalHeaderLabels(["ID", "Ragione Sociale", "Indirizzo_1", "Indirizzo_2"])
        header = self.destinazioniTable.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.destinazioniTable.cellDoubleClicked.connect(self.table_double_click)

        self.entrySearchLabel = QLabel("Cerca Destinazione")
        self.entrySearch = QLineEdit()
        self.entrySearch.textChanged.connect(self.search_destinazioni)



    def layouts(self):
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.topLayout.addWidget(self.entrySearchLabel)
        self.topLayout.addWidget(self.entrySearch)
        self.topLayout.addWidget(self.btnAddDestinazione)
        self.topLayout.addWidget(self.btnExit)
        self.bottomLayout.addWidget(self.destinazioniTable)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def load_data(self):
        self.destinazioniTable.setRowCount(0)
        destinazioni = self.session.query(Destinazione).all()
        for destinazione in destinazioni:
            self.add_row(destinazione)
        self.destinazioniTable.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def add_row(self, destinazione):
        row_position = self.destinazioniTable.rowCount()
        self.destinazioniTable.insertRow(row_position)
        self.destinazioniTable.setItem(row_position, 0, QTableWidgetItem(str(destinazione.id)))
        self.destinazioniTable.setItem(row_position, 1, QTableWidgetItem(destinazione.ragione_sociale))
        self.destinazioniTable.setItem(row_position, 2, QTableWidgetItem(destinazione.indirizzo_1))
        self.destinazioniTable.setItem(row_position, 3, QTableWidgetItem(destinazione.indirizzo_2))

    def search_destinazioni(self):
        search_text = self.entrySearch.text()
        destinazioni = self.session.query(Destinazione).filter(
            Destinazione.ragione_sociale.like(f'%{search_text}%')).all()
        self.destinazioniTable.setRowCount(0)
        for destinazione in destinazioni:
            self.add_row(destinazione)

    def table_double_click(self, row, column):
        item_id = self.destinazioniTable.item(row, 0)
        if item_id:
            destinazione_id = int(item_id.text())
            destinazione = self.session.query(Destinazione).filter_by(id=destinazione_id).first()
            if destinazione:
                self.crud_destinazione.load_data(destinazione)
                self.crud_destinazione.show()


    def openAddDestinazioneWindow(self):
        self.crud_destinazione.show()

    def openEditDestinazioneWindow(self):
        pass