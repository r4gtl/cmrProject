from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from custom_buttons import SearchButton, setup_toolbar
from db.models import SessionLocal, Destinatario, Destinazione, Trasportatore, Utente, Cmr
from gui.dialogs.search_dialog_base import SearchDialog
from utils import center
from datetime import datetime, date


class AddCmr(QMainWindow):
    def __init__(self, cmr_id=None):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 1000, 750)
        self.setFixedSize(self.size())
        center(self)
        self.session = SessionLocal()
        self.cmr_id = cmr_id

        self.UI()

    def UI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)  # Imposta il widget centrale
        self.createWidgets()
        self.createLayouts()
        self.tb = setup_toolbar(self)
        self.addToolBar(self.tb)
        if self.cmr_id:
            self.loadCmrData()
        else:
            self.loadDefaultUser()


    def createWidgets(self):
        self.createGroupBoxes()
        self.createTopWidgets()
        self.createMiddleWidgets()
        self.createBottomWidgets()

    def createGroupBoxes(self):
        self.groupUtente = QGroupBox("Mittente")
        self.groupDestinatario = QGroupBox("Destinatario")
        self.groupDestinazione = QGroupBox("Destinazione")
        self.groupTrasportatore = QGroupBox("Trasportatore")
        self.groupLuogoDataPresa = QGroupBox("Luogo e data presa in carico")
        self.groupDocumenti = QGroupBox("Documenti allegati")
        self.groupIstruzioniMittente = QGroupBox("Istruzioni Mittente")
        self.groupIstruzioniPagamento = QGroupBox("Istruzioni Pagamento")
        self.groupRimborso = QGroupBox("Rimborso")
        self.groupOsservazioni = QGroupBox("Osservazioni Trasportatore")
        self.groupConvenzioni = QGroupBox("Convenzioni")
        self.groupCompilazione = QGroupBox("Compilazione")

    def createTopWidgets(self):
        # Utente
        self.lblUtenteId = QLabel("ID:")
        self.editUtenteId = QLineEdit()
        self.editUtenteId.setReadOnly(True)
        self.editUtenteId.setStyleSheet("background-color: lightgray;")
        self.editUtenteId.setMaximumWidth(50)
        self.editUtenteId.setAlignment(Qt.AlignLeft)
        self.btnSearchMittente = SearchButton()
        self.lblRagioneSocialeUtente = QLabel("Ragione Sociale:")
        self.editRagioneSocialeUtente = QLineEdit()


        # Destinatario
        self.lblDestinatarioId = QLabel("ID:")
        self.editDestinatarioId = QLineEdit()
        self.editDestinatarioId.setReadOnly(True)
        self.editDestinatarioId.setStyleSheet("background-color: lightgray;")
        self.editDestinatarioId.setMaximumWidth(50)
        self.editDestinatarioId.setAlignment(Qt.AlignLeft)
        self.btnSearchDestinatario = SearchButton()
        self.lblRagioneSociale = QLabel("Ragione Sociale:")
        self.editRagioneSociale = QLineEdit()
        self.editRagioneSociale.setReadOnly(True)
        self.lblIndirizzo1 = QLabel("Indirizzo 1:")
        self.editIndirizzo1 = QLineEdit()
        self.editIndirizzo1.setReadOnly(True)
        self.lblIndirizzo2 = QLabel("Indirizzo 2:")
        self.editIndirizzo2 = QLineEdit()
        self.editIndirizzo2.setReadOnly(True)

        # Destinazione
        self.lblDestinazioneId = QLabel("ID:")
        self.editDestinazioneId = QLineEdit()
        self.editDestinazioneId.setReadOnly(True)
        self.editDestinazioneId.setStyleSheet("background-color: lightgray;")
        self.editDestinazioneId.setMaximumWidth(50)
        self.editDestinazioneId.setAlignment(Qt.AlignLeft)
        self.btnSearchDestinazione = SearchButton()
        self.lblRagioneSocialeDestinazione = QLabel("Ragione Sociale:")
        self.editRagioneSocialeDestinazione = QLineEdit()
        self.editRagioneSocialeDestinazione.setReadOnly(True)
        self.lblIndirizzo1Destinazione = QLabel("Indirizzo 1:")
        self.editIndirizzo1Destinazione = QLineEdit()
        self.editIndirizzo1Destinazione.setReadOnly(True)
        self.lblIndirizzo2Destinazione = QLabel("Indirizzo 2:")
        self.editIndirizzo2Destinazione = QLineEdit()
        self.editIndirizzo2Destinazione.setReadOnly(True)

        # Trasportatore
        self.lblTrasportatoreId = QLabel("ID:")
        self.editTrasportatoreId = QLineEdit()
        self.editTrasportatoreId.setReadOnly(True)
        self.editTrasportatoreId.setStyleSheet("background-color: lightgray;")
        self.editTrasportatoreId.setMaximumWidth(50)
        self.editTrasportatoreId.setAlignment(Qt.AlignLeft)
        self.btnSearchTrasportatore = SearchButton()
        self.lblRagioneSocialeTrasportatore = QLabel("Ragione Sociale:")
        self.editRagioneSocialeTrasportatore = QLineEdit()
        self.editRagioneSocialeTrasportatore.setReadOnly(True)
        self.lblIndirizzo1Trasportatore = QLabel("Indirizzo 1:")
        self.editIndirizzo1Trasportatore = QLineEdit()
        self.editIndirizzo1Trasportatore.setReadOnly(True)
        self.lblIndirizzo2Trasportatore = QLabel("Indirizzo 2:")
        self.editIndirizzo2Trasportatore = QLineEdit()
        self.editIndirizzo2Trasportatore.setReadOnly(True)

        # Luogo e Data Presa in Carico
        self.lblLuogoPresa = QLabel("Luogo")
        self.editLuogoPresa = QLineEdit()
        self.lblDataPresa = QLabel("Data")
        self.editDataPresa = QLineEdit()

        # Documenti Allegati
        self.lblDocumenti = QLabel("Documenti Allegati")
        self.editDocumenti = QLineEdit()

        # Istruzioni Mittente
        self.lblIstruzioniMittente = QLabel("Istruzioni Mittente")
        self.editIstruzioniMittente = QLineEdit()

        # Istruzioni Pagamento
        self.lblIstruzioniPagamento = QLabel("Istruzioni Pagamento")
        self.editIstruzioniPagamento = QLineEdit()
        self.checkPortoFranco = QCheckBox("Porto Franco")
        self.checkPortoAssegnato = QCheckBox("Porto Assegnato")

        # Rimborso
        self.lblRimborso = QLabel("Rimborso")
        self.editRimborso = QLineEdit()

        # Update Button
        self.btnUpdate = QPushButton("Update Data")

    def createMiddleWidgets(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Unità di Misura", "Numero Colli", "Imballaggio", "Descrizione", "Statistica", "Peso lordo (Kg)",
             "Volume (MC)"]
        )
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

    def createBottomWidgets(self):
        self.lblOsservazioni = QLabel("Osservazioni")
        self.editOsservazioni = QLineEdit()
        self.lblConvenzioni = QLabel("Convenzioni")
        self.editConvenzioni = QLineEdit()
        self.lblLuogoCompilazione = QLabel("Luogo Compilazione")
        self.editLuogoCompilazione = QLineEdit()
        self.lblDataCompilazione = QLabel("Data Compilazione")
        self.editDataCompilazione = QLineEdit()

    def createLayouts(self):
        self.mainLayout = QVBoxLayout(self.centralWidget())
        self.createTopLayout()
        self.createMiddleLayout()
        self.createBottomLayout()



        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.table)
        self.mainLayout.addLayout(self.bottomLayout)

    def createTopLayout(self):
        self.topLayout = QGridLayout()

        self.createMittenteLayout()
        self.createDestinatarioLayout()
        self.createDestinazioneLayout()
        self.createTrasportatoreLayout()



        self.topLayout.addWidget(self.groupUtente, 0, 0)
        self.topLayout.addWidget(self.groupDestinatario, 0, 1)
        self.topLayout.addWidget(self.groupDestinazione, 0, 2)
        self.topLayout.addWidget(self.groupTrasportatore, 0, 3, 1, 2)

    def createMittenteLayout(self):
        self.mittenteLayout = QVBoxLayout(self.groupUtente)
        self.mittenteFormLayout = QFormLayout()
        self.mittenteFormLayout.addRow(self.btnSearchMittente)
        self.mittenteFormLayout.addRow(self.lblUtenteId, self.editUtenteId)
        self.mittenteFormLayout.addRow(self.lblRagioneSocialeUtente, self.editRagioneSocialeUtente)
        self.mittenteLayout.addLayout(self.mittenteFormLayout)

    def createDestinatarioLayout(self):
        self.destinatarioLayout = QVBoxLayout(self.groupDestinatario)
        self.destinatarioFormLayout = QFormLayout()
        self.destinatarioFormLayout.addRow(self.btnSearchDestinatario)
        self.destinatarioFormLayout.addRow(self.lblDestinatarioId, self.editDestinatarioId)
        self.destinatarioFormLayout.addRow(self.lblRagioneSociale, self.editRagioneSociale)
        self.destinatarioFormLayout.addRow(self.lblIndirizzo1, self.editIndirizzo1)
        self.destinatarioFormLayout.addRow(self.lblIndirizzo2, self.editIndirizzo2)
        self.destinatarioLayout.addLayout(self.destinatarioFormLayout)
        self.btnSearchDestinatario.clicked.connect(self.update_destinatario_data)

    def createDestinazioneLayout(self):
        self.destinazioneLayout = QVBoxLayout(self.groupDestinazione)
        self.destinazioneFormLayout = QFormLayout()
        self.destinazioneFormLayout.addRow(self.btnSearchDestinazione)
        self.destinazioneFormLayout.addRow(self.lblDestinazioneId, self.editDestinazioneId)
        self.destinazioneFormLayout.addRow(self.lblRagioneSocialeDestinazione, self.editRagioneSocialeDestinazione)
        self.destinazioneFormLayout.addRow(self.lblIndirizzo1Destinazione, self.editIndirizzo1Destinazione)
        self.destinazioneFormLayout.addRow(self.lblIndirizzo2Destinazione, self.editIndirizzo2Destinazione)
        self.destinazioneLayout.addLayout(self.destinazioneFormLayout)
        self.btnSearchDestinazione.clicked.connect(self.update_destinazione_data)

    def createTrasportatoreLayout(self):
        self.trasportatoreLayout = QVBoxLayout(self.groupTrasportatore)
        self.trasportatoreFormLayout = QFormLayout()
        self.trasportatoreFormLayout.addRow(self.btnSearchTrasportatore)
        self.trasportatoreFormLayout.addRow(self.lblTrasportatoreId, self.editTrasportatoreId)
        self.trasportatoreFormLayout.addRow(self.lblRagioneSocialeTrasportatore, self.editRagioneSocialeTrasportatore)
        self.trasportatoreFormLayout.addRow(self.lblIndirizzo1Trasportatore, self.editIndirizzo1Trasportatore)
        self.trasportatoreFormLayout.addRow(self.lblIndirizzo2Trasportatore, self.editIndirizzo2Trasportatore)
        self.trasportatoreLayout.addLayout(self.trasportatoreFormLayout)
        self.btnSearchTrasportatore.clicked.connect(self.update_trasportatore_data)

    def createMiddleLayout(self):
        pass  # Già gestito con il QTableWidget

    def createBottomLayout(self):
        self.bottomLayout = QVBoxLayout()

        self.osservazioniLayout = QHBoxLayout()
        self.osservazioniLayout.addWidget(self.lblOsservazioni)
        self.osservazioniLayout.addWidget(self.editOsservazioni)

        self.convenzioniLayout = QHBoxLayout()
        self.convenzioniLayout.addWidget(self.lblConvenzioni)
        self.convenzioniLayout.addWidget(self.editConvenzioni)

        self.compilazioneLayout = QHBoxLayout()
        self.compilazioneLayout.addWidget(self.lblLuogoCompilazione)
        self.compilazioneLayout.addWidget(self.editLuogoCompilazione)
        self.compilazioneLayout.addWidget(self.lblDataCompilazione)
        self.compilazioneLayout.addWidget(self.editDataCompilazione)

        self.bottomLayout.addLayout(self.osservazioniLayout)
        self.bottomLayout.addLayout(self.convenzioniLayout)
        self.bottomLayout.addLayout(self.compilazioneLayout)
        self.bottomLayout.addWidget(self.btnUpdate)

    def update_utente_data(self):
        # Implement logic to fetch and display Utente data based on ID
        pass

    # def update_destinatario_data(self):

    #   destinatari = self.session.query(Destinatario).all()
    #   print(f"Destrinatari: {destinatari}")#

    #   dialog = RicercaDestinatario(destinatari)
    #   dialog.destinatario_selected.connect(self.set_destinatario_id)
    #   dialog.exec_()

    def update_destinatario_data(self):
        destinatari = self.session.query(Destinatario).all()
        items = [(d.id, d.ragione_sociale, d.indirizzo_1, d.indirizzo_2) for d in destinatari]
        headers = ["ID", "Ragione Sociale", "Indirizzo 1", "Indirizzo 2"]
        dialog = SearchDialog(items, headers, search_field="Ragione Sociale")
        dialog.item_selected.connect(self.set_destinatario_data)
        dialog.exec_()

    def set_destinatario_data(self, id):
        destinatario = self.session.query(Destinatario).get(id)
        if destinatario:
            self.editDestinatarioId.setText(str(destinatario.id))
            self.editRagioneSociale.setText(destinatario.ragione_sociale)
            self.editIndirizzo1.setText(destinatario.indirizzo_1)
            self.editIndirizzo2.setText(destinatario.indirizzo_2)

    def set_destinatario_id(self, destinatario_id):
        self.editDestinatarioId.setText(str(destinatario_id))
        self.load_destinatario_details(destinatario_id)

    def load_destinatario_details(self, destinatario_id):
        destinatario = self.session.query(Destinatario).filter(Destinatario.id == destinatario_id).first()
        if destinatario:
            self.editRagioneSociale.setText(destinatario.ragione_sociale)
            self.editIndirizzo1.setText(destinatario.indirizzo_1)
            self.editIndirizzo2.setText(destinatario.indirizzo_2)

    def update_trasportatore_data(self):
        trasportatori = self.session.query(Trasportatore).all()
        items = [(t.id, t.ragione_sociale, t.indirizzo_1, t.indirizzo_2) for t in trasportatori]
        headers = ["ID", "Ragione Sociale", "Indirizzo 1", "Indirizzo 2"]
        dialog = SearchDialog(items, headers, search_field="Ragione Sociale")
        dialog.item_selected.connect(self.set_trasportatore_data)
        dialog.exec_()

    def set_trasportatore_data(self, id):
        trasportatore = self.session.query(Trasportatore).get(id)
        if trasportatore:
            self.editTrasportatoreId.setText(str(trasportatore.id))
            self.editRagioneSocialeTrasportatore.setText(trasportatore.ragione_sociale)
            self.editIndirizzo1Trasportatore.setText(trasportatore.indirizzo_1)
            self.editIndirizzo2Trasportatore.setText(trasportatore.indirizzo_2)

    def update_destinazione_data(self):
        destinazioni = self.session.query(Destinazione).all()
        items = [(d.id, d.ragione_sociale, d.indirizzo_1, d.indirizzo_2) for d in destinazioni]
        headers = ["ID", "Ragione Sociale", "Indirizzo 1", "Indirizzo 2"]
        dialog = SearchDialog(items, headers, search_field="Ragione Sociale")
        dialog.item_selected.connect(self.set_destinazione_data)
        dialog.exec_()

    def set_destinazione_data(self, id):
        destinazione = self.session.query(Destinazione).get(id)
        if destinazione:
            self.editDestinazioneId.setText(str(destinazione.id))
            self.editRagioneSocialeDestinazione.setText(destinazione.ragione_sociale)
            self.editIndirizzo1Destinazione.setText(destinazione.indirizzo_1)
            self.editIndirizzo2Destinazione.setText(destinazione.indirizzo_2)

    def loadDefaultUser(self):
        user = self.session.query(Utente).first()
        if user:
            self.editUtenteId.setText(str(user.id))
            self.editRagioneSocialeUtente.setText(user.nome)

    def loadCmrData(self):
        cmr = self.session.query(Cmr).filter(Cmr.id == self.cmr_id).first()
        if cmr:
            # Mittente
            self.editUtenteId.setText(str(cmr.mittente_id))
            user = self.session.query(Utente).filter(Utente.id == cmr.mittente_id).first()
            if user:
                self.editRagioneSocialeUtente.setText(user.nome)

            # Destinatario
            self.editDestinatarioId.setText(str(cmr.destinatario_id))
            destinatario = self.session.query(Destinatario).filter(Destinatario.id == cmr.destinatario_id).first()
            if destinatario:
                self.editRagioneSociale.setText(destinatario.ragione_sociale)
                self.editIndirizzo1.setText(destinatario.indirizzo1)
                self.editIndirizzo2.setText(destinatario.indirizzo2)

            # Destinazione
            self.editDestinazioneId.setText(str(cmr.destinazione_id))
            destinazione = self.session.query(Destinazione).filter(Destinazione.id == cmr.destinazione_id).first()
            if destinazione:
                self.editRagioneSocialeDestinazione.setText(destinazione.ragione_sociale)
                self.editIndirizzo1Destinazione.setText(destinazione.indirizzo1)
                self.editIndirizzo2Destinazione.setText(destinazione.indirizzo2)

            # Trasportatore
            self.editTrasportatoreId.setText(str(cmr.trasportatore_id))
            trasportatore = self.session.query(Trasportatore).filter(Trasportatore.id == cmr.trasportatore_id).first()
            if trasportatore:
                self.editRagioneSocialeTrasportatore.setText(trasportatore.ragione_sociale)
                self.editIndirizzo1Trasportatore.setText(trasportatore.indirizzo1)
                self.editIndirizzo2Trasportatore.setText(trasportatore.indirizzo2)

    def addSave(self):

        if self.validateCmrData():
            cmr_data = {
                'utente_id': int(self.editUtenteId.text()),
                'destinatario_id': int(self.editDestinatarioId.text()),
                'destinazione_id': int(self.editDestinazioneId.text()),
                'luogo_presa_in_carico': self.editLuogoPresa.text(),
                'data_presa_in_carico': datetime.strptime(self.editDataPresa.text(), '%d/%m/%Y').date(),
                'documenti_allegati': self.editDocumenti.text(),
                'istruzioni_mittente': self.editIstruzioniMittente.text(),
                'porto_franco': self.checkPortoFranco.isChecked(),
                'porto_assegnato': self.checkPortoAssegnato.isChecked(),
                'rimborso': self.editRimborso.text(),
                'trasportatore_id': int(self.editTrasportatoreId.text()),
                'osservazioni_trasporto': self.editOsservazioni.text(),
                'convenzioni': self.editConvenzioni.text(),
                'compilato_a': self.editLuogoCompilazione.text(),
                'data_compilazione': datetime.strptime(self.editDataCompilazione.text(), '%d/%m/%Y').date()
            }
            new_cmr = Cmr(**cmr_data)
            if new_cmr.save_cmr_data():
                print("Arrivato qui! Salvataggio corretto!")
                QMessageBox.information(self, "Salva", "Dati CMR salvati con successo!")
                self.close()
            else:
                print("Arrivato qui! Salvataggio sbagliato!")
                QMessageBox.warning(self, "Errore", "Errore durante il salvataggio dei dati del CMR.")

    def validateCmrData(self):
        # Validazione dell'utente
        utente_id = self.editUtenteId.text()
        if not utente_id:
            QMessageBox.warning(self, "Errore", "ID Utente non specificato.")
            return False

        # Validazione del destinatario
        destinatario_id = self.editDestinatarioId.text()
        if not destinatario_id:
            QMessageBox.warning(self, "Errore", "ID Destinatario non specificato.")
            return False

        # Validazione della destinazione
        destinazione_id = self.editDestinazioneId.text()
        if not destinazione_id:
            QMessageBox.warning(self, "Errore", "ID Destinazione non specificato.")
            return False

        # Validazione del luogo di presa in carico
        # luogo_presa = self.editLuogoPresa.text()
        # if not luogo_presa:
        #     QMessageBox.warning(self, "Errore", "Luogo di presa in carico non specificato.")
        #     return False
        #
        # # Validazione della data di presa in carico
        # data_presa = self.editDataPresa.text()
        # if not data_presa:
        #     QMessageBox.warning(self, "Errore", "Data di presa in carico non specificata.")
        #     return False

        # Altri campi possono essere validati secondo necessità...

        return True