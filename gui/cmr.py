import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from utils import center
from custom_buttons import SearchButton
from gui.ricercaDestinatario import RicercaDestinatario
from db.models import SessionLocal, Destinatario



class AddCmr(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1000,750)
        self.setFixedSize(self.size())
        center(self)
        self.central_widget = QWidget()  # Creazione del widget centrale
        self.setCentralWidget(self.central_widget)  # Impostazione del widget centrale
        self.session = SessionLocal()

        self.UI()

        if self.editDestinatarioId.text():
            destinatario_id = int(self.editDestinatarioId.text())
            self.load_destinatario_details(destinatario_id)

        #self.show()


    def UI(self):
        self.widgets()
        self.layouts()
        self.toolBar()

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.layout.addWidget(self.tb)  # Aggiunta della toolbar al layout
        #self.layout.addStretch()  # Aggiunta di uno spacer per spingere il contenuto in basso

        # ToolBar Buttons
        # New CMR
        self.addSave = QAction(QIcon('icons/save.png'), "Salva", self)
        self.tb.addAction(self.addSave)
        # self.addSave.triggered.connect(self.funcaddSave)
        self.tb.addSeparator()
        self.deleteCmr = QAction(QIcon('icons/delete-folder.png'), "Elimina", self)
        self.tb.addAction(self.deleteCmr)
        # self.deleteCmr.triggered.connect(self.funcdeleteCmr)
        self.tb.addSeparator()
        self.exit = QAction(QIcon('icons/exit.png'), "Esci", self)
        self.exit.triggered.connect(self.close)
        self.tb.addAction(self.exit)
        # self.exit.triggered.connect(self.funcexit)
        self.tb.addSeparator()


    def widgets(self):
        self.btnUtente = QPushButton("Mittente")
        self.btnDestinatario = QPushButton("Destinatario")
        self.btnDestinazione = QPushButton("Destinazione")

        self.groupUtente = QGroupBox("Mittente")
        self.groupDestinatario = QGroupBox("Destinatario")
        self.groupDestinazione = QGroupBox("Destinazione")


        self.lblUtenteId = QLabel("ID:")
        self.editUtenteId = QLineEdit()

        self.lblDestinatarioId = QLabel("ID:")
        self.lblDestinatarioId.setMaximumWidth(50)
        self.lblDestinatarioId.setAlignment(Qt.AlignLeft)

        self.editDestinatarioId = QLineEdit()
        self.editDestinatarioId.setReadOnly(True)  # Imposta il QLineEdit come non modificabile
        self.editDestinatarioId.setStyleSheet("background-color: lightgray;")  # Cambia lo stile per indicare non modificabile
        self.editDestinatarioId.setMaximumWidth(50)  # Imposta la larghezza massima
        self.editDestinatarioId.setAlignment(Qt.AlignLeft)
        self.lblRagioneSociale = QLabel("Ragione Sociale:")
        self.editRagioneSociale = QLineEdit()
        self.editRagioneSociale.setReadOnly(True)

        self.lblIndirizzo1 = QLabel("Indirizzo 1:")
        self.editIndirizzo1 = QLineEdit()
        self.editIndirizzo1.setReadOnly(True)

        self.lblIndirizzo2 = QLabel("Indirizzo 2:")
        self.editIndirizzo2 = QLineEdit()
        self.editIndirizzo2.setReadOnly(True)


        self.lblDestinazioneId = QLabel("ID:")
        self.editDestinazioneId = QLineEdit()

        self.btnUpdate = QPushButton("Update Data")
        self.btnSearchMittente = QPushButton("Search")
        self.btnSearchDestinatario = SearchButton()

        self.btnSearchDestinazione = QPushButton("Search")

        self.groupLuogoDataPresa = QGroupBox("Luogo e data presa in carico")
        self.groupDocumenti = QGroupBox("Documenti allegati")
        self.groupIstruzioniMittente = QGroupBox("Istruzioni Mittente")
        self.groupIstruzioniPagamento = QGroupBox("Istruzioni Pagamento")
        self.groupRimborso = QGroupBox("Rimborso")

        self.lblLuogoPresa = QLabel("Luogo")
        self.editLuogoPresa = QLineEdit()
        self.lblDataPresa = QLabel("Data")
        self.editDataPresa = QLineEdit()

        self.lblDocumenti = QLabel("Documenti Allegati")
        self.editDocumenti = QLineEdit()

        self.lblIstruzioniMittente = QLabel("Istruzioni Mittente")
        self.editIstruzioniMittente = QLineEdit()

        self.lblIstruzioniPagamento = QLabel("Istruzioni Pagamento")
        self.editIstruzioniPagamento = QLineEdit()

        self.checkPortoFranco = QCheckBox("Porto Franco")
        self.checkPortoAssegnato = QCheckBox("Porto Assegnato")

        self.lblRimborso = QLabel("Rimborso")
        self.editRimborso = QLineEdit()




        self.groupTrasportatore = QGroupBox("Trasportatore")
        self.groupOsservazioni = QGroupBox("Osservazioni Trasportatore")
        self.groupConvenzioni = QGroupBox("Convenzioni")
        self.groupCompilazione = QGroupBox("Compilazione")

        self.lblTrasportatoreId = QLabel("ID:")
        self.editTrasportatoreId = QLineEdit()

        self.lblOsservazioni = QLabel("Osservazioni")
        self.editOsservazioni = QLineEdit()

        self.lblConvenzioni = QLabel("Convenzioni")
        self.editConvenzioni = QLineEdit()

        self.lblLuogoCompilazione = QLabel("Luogo Compilazione")
        self.editLuogoCompilazione = QLineEdit()

        self.lblDataCompilazione = QLabel("Data Compilazione")
        self.editDataCompilazione = QLineEdit()

        # Preparo la tabella per il middleLayout
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Unità di Misura", "Numero Colli", "Imballaggio", "Descrizione", "Statistica", "Peso lordo (Kg)", "Volume (MC)"])
        # self.table.horizontalHeader().setStretchLastSection(True)  # Make the last column stretchable
        # self.table.horizontalHeader().setSectionResizeMode(QTableWidget.Stretch)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)




    def layouts(self):
        #self.layout = QVBoxLayout()  # Creazione del layout verticale
        #self.setLayout(self.layout)  # Impostazione del layout per il widget

        self.mainLayout = QVBoxLayout(self.central_widget)
        self.topLayout = QHBoxLayout()
        self.middleLayout = QVBoxLayout()
        self.bottomLayout = QHBoxLayout()

        self.gridTopLayout = QGridLayout()

        # preparo i layout per il top layout
        self.layoutUtente = QHBoxLayout()
        self.layoutDestinatario = QHBoxLayout()
        self.layoutDestinatarioDetails = QVBoxLayout()
        self.layoutDestinazione = QVBoxLayout()
        self.layoutLuogoDataPresa = QVBoxLayout()
        self.layoutDocumenti = QHBoxLayout()
        self.layoutIstruzioniMittente = QHBoxLayout()
        self.layoutIstruzioniPagamento = QVBoxLayout()
        self.layoutRimborso = QHBoxLayout()


        self.layoutUtente.addWidget(self.lblUtenteId)
        self.layoutUtente.addWidget(self.btnSearchMittente)
        self.layoutUtente.addWidget(self.editUtenteId)
        self.groupUtente.setLayout(self.layoutUtente)

        self.layoutDestinatario.addWidget(self.lblDestinatarioId)
        self.layoutDestinatario.addWidget(self.btnSearchDestinatario)
        self.layoutDestinatario.addWidget(self.editDestinatarioId)
        #self.groupDestinatario.setLayout(self.layoutDestinatario)

        self.layoutDestinatarioDetails.addWidget(self.lblRagioneSociale)
        self.layoutDestinatarioDetails.addWidget(self.editRagioneSociale)
        self.layoutDestinatarioDetails.addWidget(self.lblIndirizzo1)
        self.layoutDestinatarioDetails.addWidget(self.editIndirizzo1)
        self.layoutDestinatarioDetails.addWidget(self.lblIndirizzo2)
        self.layoutDestinatarioDetails.addWidget(self.editIndirizzo2)
        #self.groupDestinatario.setLayout(self.layoutDestinatarioDetails)

        self.layoutDestinatarioInner = QVBoxLayout()
        self.layoutDestinatarioInner.addLayout(self.layoutDestinatario)
        self.layoutDestinatarioInner.addLayout(self.layoutDestinatarioDetails)
        self.groupDestinatario.setLayout(self.layoutDestinatarioInner)

        self.layoutDestinazione.addWidget(self.lblDestinazioneId)
        self.layoutDestinazione.addWidget(self.btnSearchDestinazione)
        self.layoutDestinazione.addWidget(self.editDestinazioneId)
        self.groupDestinazione.setLayout(self.layoutDestinazione)

        self.layoutLuogoDataPresa.addWidget(self.lblLuogoPresa)
        self.layoutLuogoDataPresa.addWidget(self.editLuogoPresa)
        self.layoutLuogoDataPresa.addWidget(self.lblDataPresa)
        self.layoutLuogoDataPresa.addWidget(self.editDataPresa)
        self.groupLuogoDataPresa.setLayout(self.layoutLuogoDataPresa)

        self.layoutDocumenti.addWidget(self.lblDocumenti)
        self.layoutDocumenti.addWidget(self.editDocumenti)
        self.groupDocumenti.setLayout(self.layoutDocumenti)

        self.layoutIstruzioniMittente.addWidget(self.lblIstruzioniMittente)
        self.layoutIstruzioniMittente.addWidget(self.editIstruzioniMittente)
        self.groupIstruzioniMittente.setLayout(self.layoutIstruzioniMittente)

        self.layoutIstruzioniPagamento.addWidget(self.checkPortoFranco)
        self.layoutIstruzioniPagamento.addWidget(self.checkPortoAssegnato)
        self.groupIstruzioniPagamento.setLayout(self.layoutIstruzioniPagamento)

        self.layoutRimborso.addWidget(self.lblRimborso)
        self.layoutRimborso.addWidget(self.editRimborso)
        self.groupRimborso.setLayout(self.layoutRimborso)


        self.gridTopLayout.addWidget(self.groupUtente, 0,0)
        self.gridTopLayout.addWidget(self.groupDestinatario, 0,1)
        self.gridTopLayout.addWidget(self.groupDestinazione, 0,2)
        self.gridTopLayout.addWidget(self.groupLuogoDataPresa, 1,0)
        self.gridTopLayout.addWidget(self.groupDocumenti, 1,1)
        self.gridTopLayout.addWidget(self.groupIstruzioniMittente, 1,2)
        self.gridTopLayout.addWidget(self.groupIstruzioniPagamento, 1,3)
        self.gridTopLayout.addWidget(self.groupRimborso, 1,4)


        # Preparo i layout per il bottom layout
        self.layoutTrasportatore = QHBoxLayout()
        self.layoutOsservazioni = QHBoxLayout()
        self.layoutConvenzioni = QHBoxLayout()
        self.layoutCompilazione = QHBoxLayout()

        self.layoutTrasportatore.addWidget(self.lblTrasportatoreId)
        self.layoutTrasportatore.addWidget(self.editTrasportatoreId)
        self.groupTrasportatore.setLayout(self.layoutTrasportatore)

        self.layoutOsservazioni.addWidget(self.lblOsservazioni)
        self.layoutOsservazioni.addWidget(self.editOsservazioni)
        self.groupOsservazioni.setLayout(self.layoutOsservazioni)

        self.layoutConvenzioni.addWidget(self.lblConvenzioni)
        self.layoutConvenzioni.addWidget(self.editConvenzioni)
        self.groupConvenzioni.setLayout(self.layoutConvenzioni)

        self.layoutCompilazione.addWidget(self.lblLuogoCompilazione)
        self.layoutCompilazione.addWidget(self.editLuogoCompilazione)
        self.layoutCompilazione.addWidget(self.lblDataCompilazione)
        self.layoutCompilazione.addWidget(self.editDataCompilazione)
        self.groupCompilazione.setLayout(self.layoutCompilazione)





        # self.topLayout.addWidget(self.groupUtente)
        # self.topLayout.addWidget(self.groupDestinatario)
        # self.topLayout.addWidget(self.groupDestinazione)

        self.topLayout.addLayout(self.gridTopLayout)

        self.middleLayout.addWidget(self.table)

        self.bottomLayout.addWidget(self.groupTrasportatore)
        self.bottomLayout.addWidget(self.groupOsservazioni)
        self.bottomLayout.addWidget(self.groupConvenzioni)
        self.bottomLayout.addWidget(self.groupCompilazione)
        self.bottomLayout.addWidget(self.btnUpdate)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.btnUtente.clicked.connect(self.update_utente_data)
        self.btnDestinatario.clicked.connect(self.update_destinatario_data)
        self.btnSearchDestinatario.clicked.connect(self.update_destinatario_data)
        self.btnDestinazione.clicked.connect(self.update_destinazione_data)
        self.btnUpdate.clicked.connect(self.update_data_from_id)

    def update_utente_data(self):
        # Implement logic to fetch and display Utente data based on ID
        pass

    def update_destinatario_data(self):

        destinatari = self.session.query(Destinatario).all()
        print(f"Destrinatari: {destinatari}")

        dialog = RicercaDestinatario(destinatari)
        dialog.destinatario_selected.connect(self.set_destinatario_id)
        dialog.exec_()

    def update_destinazione_data(self):
        # Implement logic to fetch and display Destinazione data based on ID
        pass

    def update_data_from_id(self):
        # Implement logic to update data based on the entered IDs
        pass

    def set_destinatario_id(self, destinatario_id):
        self.editDestinatarioId.setText(str(destinatario_id))
        self.load_destinatario_details(destinatario_id)

    def load_destinatario_details(self, destinatario_id):
        destinatario = self.session.query(Destinatario).filter(Destinatario.id == destinatario_id).first()
        if destinatario:
            self.editRagioneSociale.setText(destinatario.ragione_sociale)
            self.editIndirizzo1.setText(destinatario.indirizzo_1)
            self.editIndirizzo2.setText(destinatario.indirizzo_2)

