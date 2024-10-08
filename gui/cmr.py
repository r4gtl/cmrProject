from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate
from custom_buttons import SearchButton, setup_toolbar, AddButton
from db.models import SessionLocal, Destinatario, Destinazione, Trasportatore, Utente, Cmr, DettaglioCmr
from gui.dialogs.search_dialog_base import SearchDialog
from gui.add_cmr_details import CrudDettaglioCmr
from utils import center
from datetime import datetime, date
import sys
import subprocess
import os
# Importa PROJECT_DIR dal modulo di configurazione
from settings import PROJECT_DIR


class AddCmr(QMainWindow):
    def __init__(self, cmr_id=None):
        super().__init__()
        self.setWindowTitle("CMR Manager")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450, 150, 1500, 750)
        #self.setFixedSize(self.size())
        self.add_details = CrudDettaglioCmr()
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
        self.editDataPresa = QDateEdit()
        self.editDataPresa.setDisplayFormat("dd/MM/yyyy")
        self.editDataPresa.setCalendarPopup(True)  # Per mostrare il calendario a popup (opzionale)
        self.editDataPresa.setDate(QDate.currentDate())

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
        self.btnAddDetail = AddButton()
        self.btnAddDetail.clicked.connect(self.addDetail)

    def createBottomWidgets(self):
        self.lblOsservazioni = QLabel("Osservazioni")
        self.editOsservazioni = QLineEdit()
        self.lblConvenzioni = QLabel("Convenzioni")
        self.editConvenzioni = QLineEdit()
        self.lblLuogoCompilazione = QLabel("Luogo Compilazione")
        self.editLuogoCompilazione = QLineEdit()
        self.lblDataCompilazione = QLabel("Data Compilazione")
        self.editDataCompilazione = QDateEdit()
        self.editDataCompilazione.setDisplayFormat("dd/MM/yyyy")
        self.editDataCompilazione.setCalendarPopup(True)  # Per mostrare il calendario a popup (opzionale)
        self.editDataCompilazione.setDate(QDate.currentDate())

    def createLayouts(self):
        self.mainLayout = QVBoxLayout(self.centralWidget())
        self.createTopLayout()
        self.createMiddleLayout()
        self.createBottomLayout()



        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        #self.mainLayout.addWidget(self.table)
        self.mainLayout.addLayout(self.bottomLayout)

    def createTopLayout(self):
        self.topLayout = QGridLayout()

        self.createMittenteLayout()
        self.createDestinatarioLayout()
        self.createDestinazioneLayout()
        self.createTrasportatoreLayout()
        self.createLuogoDataPresaLayout()
        self.createDocumentiLayout()
        self.createIstruzioniMittenteLayout()
        self.createIstruzioniPagamentoLayout()
        self.createRimborsoLayout()



        self.topLayout.addWidget(self.groupUtente, 0, 0)
        self.topLayout.addWidget(self.groupDestinatario, 0, 1)
        self.topLayout.addWidget(self.groupDestinazione, 0, 2)
        self.topLayout.addWidget(self.groupTrasportatore, 0, 3, 1, 2)
        self.topLayout.addWidget(self.groupLuogoDataPresa, 1, 0)
        self.topLayout.addWidget(self.groupDocumenti, 1, 1)
        self.topLayout.addWidget(self.groupIstruzioniMittente, 1, 2)
        self.topLayout.addWidget(self.groupIstruzioniPagamento, 1, 3)
        self.topLayout.addWidget(self.groupRimborso, 1, 4)


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

    def createLuogoDataPresaLayout(self):
        self.luogoDataPresaLayout = QVBoxLayout(self.groupLuogoDataPresa)
        self.luogoDataPresaFormLayout = QFormLayout()
        self.luogoDataPresaFormLayout.addRow(self.lblLuogoPresa, self.editLuogoPresa)
        self.luogoDataPresaFormLayout.addRow(self.lblDataPresa, self.editDataPresa)
        self.luogoDataPresaLayout.addLayout(self.luogoDataPresaFormLayout)

    def createDocumentiLayout(self):
        self.documentiLayout =QVBoxLayout(self.groupDocumenti)
        self.documentiFormLayout = QFormLayout()
        self.documentiFormLayout.addRow(self.lblDocumenti, self.editDocumenti)
        self.documentiLayout.addLayout(self.documentiFormLayout)

    def createIstruzioniMittenteLayout(self):
        self.istruzioniMittenteLayout = QVBoxLayout(self.groupIstruzioniMittente)
        self.istruzioniMittenteFormLayout = QFormLayout()
        self.istruzioniMittenteFormLayout.addRow(self.lblIstruzioniMittente, self.editIstruzioniMittente)
        self.istruzioniMittenteLayout.addLayout(self.istruzioniMittenteFormLayout)

    def createIstruzioniPagamentoLayout(self):
        self.istruzioniPagamentoLayout = QVBoxLayout(self.groupIstruzioniPagamento)
        self.istruzioniPagamentoFormLayout = QFormLayout()
        self.istruzioniPagamentoFormLayout.addRow(self.lblIstruzioniPagamento, self.editIstruzioniPagamento)
        self.istruzioniPagamentoLayout.addLayout(self.istruzioniPagamentoFormLayout)

    def createRimborsoLayout(self):
        self.rimborsoLayout = QVBoxLayout(self.groupRimborso)
        self.rimborsoFormLayout = QFormLayout()
        self.rimborsoFormLayout.addRow(self.lblRimborso, self.editRimborso)
        self.rimborsoLayout.addLayout(self.rimborsoFormLayout)




    def createMiddleLayout(self):

        self.middleLayout = QHBoxLayout()
        self.tableLayout = QHBoxLayout()
        self.btnLayout = QVBoxLayout()

        self.tableLayout.addWidget(self.table)
        self.btnLayout.addWidget(self.btnAddDetail, alignment=Qt.AlignTop)
        self.middleLayout.addLayout(self.tableLayout)
        self.middleLayout.addLayout(self.btnLayout)


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
        print("Errore LoadCmrData")
        print(f"Cmr.id: {self.cmr_id}")
        if cmr:
            print("CMR OK")
            # Mittente
            self.editUtenteId.setText(str(cmr.utente_id))
            user = self.session.query(Utente).filter(Utente.id == cmr.utente_id).first()
            print(f"User: {user}")
            if user:
                self.editRagioneSocialeUtente.setText(user.nome)
            print("User ok")
            # Destinatario
            self.editDestinatarioId.setText(str(cmr.destinatario_id))
            try:
                destinatario = self.session.query(Destinatario).filter(Destinatario.id == cmr.destinatario_id).first()
                print(f"Destinatario: {destinatario.ragione_sociale}")
                if destinatario:
                    self.editRagioneSociale.setText(destinatario.ragione_sociale)
                    self.editIndirizzo1.setText(destinatario.indirizzo_1)
                    self.editIndirizzo2.setText(destinatario.indirizzo_2)
            except Exception as e:
                print(f"Errore durante l'accesso a Destinatario: {e}")
            print("Destinatario ok")
            # Destinazione
            self.editDestinazioneId.setText(str(cmr.destinazione_id))
            destinazione = self.session.query(Destinazione).filter(Destinazione.id == cmr.destinazione_id).first()
            if destinazione:
                self.editRagioneSocialeDestinazione.setText(destinazione.ragione_sociale)
                self.editIndirizzo1Destinazione.setText(destinazione.indirizzo_1)
                self.editIndirizzo2Destinazione.setText(destinazione.indirizzo_2)
            print("Destinazione ok")
            # Trasportatore
            self.editTrasportatoreId.setText(str(cmr.trasportatore_id))
            trasportatore = self.session.query(Trasportatore).filter(Trasportatore.id == cmr.trasportatore_id).first()
            if trasportatore:
                self.editRagioneSocialeTrasportatore.setText(trasportatore.ragione_sociale)
                self.editIndirizzo1Trasportatore.setText(trasportatore.indirizzo_1)
                self.editIndirizzo2Trasportatore.setText(trasportatore.indirizzo_2)
            print("Trasportatore ok")
            self.editLuogoPresa.setText(cmr.luogo_presa_in_carico)
            print(f"Luogo presa: {cmr.luogo_presa_in_carico}")
            self.editDataPresa.setDate(cmr.data_presa_in_carico)
            print(f"Data presa: {cmr.data_presa_in_carico}")
            self.editDocumenti.setText(cmr.documenti_allegati)
            print(f"Documenti: {cmr.documenti_allegati}")
            self.editIstruzioniMittente.setText(cmr.istruzioni_mittente)
            print(f"istruzioni_mittente: {cmr.istruzioni_mittente}")
            #self.checkPortoFranco.setChecked(cmr.porto_franco)

            #self.checkPortoAssegnato.setChecked(cmr.porto_assegnato)
            self.editRimborso.setText(cmr.rimborso)
            print(f"rimborso: {cmr.rimborso}")
            self.editOsservazioni.setText(cmr.osservazioni_trasporto)
            print(f"osservazioni_trasporto: {cmr.osservazioni_trasporto}")
            self.editConvenzioni.setText(cmr.convenzioni)
            print(f"convenzioni: {cmr.convenzioni}")
            self.editLuogoCompilazione.setText(cmr.compilato_a)
            print(f"compilato_a: {cmr.compilato_a}")
            self.editDataCompilazione.setDate(cmr.data_compilazione)
            print(f"data_compilazione: {cmr.data_compilazione}")




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
                QMessageBox.information(self, "Success", "CMR salvato con successo!")
            else:
                QMessageBox.critical(self, "Error", "Errore durante il salvataggio del CMR.")

    def validateCmrData(self):
        if not self.editUtenteId.text().isdigit():
            QMessageBox.critical(self, "Error", "ID Utente non valido.")
            return False
        if not self.editDestinatarioId.text().isdigit():
            QMessageBox.critical(self, "Error", "ID Destinatario non valido.")
            return False
        if not self.editDestinazioneId.text().isdigit():
            QMessageBox.critical(self, "Error", "ID Destinazione non valido.")
            return False
        if not self.editTrasportatoreId.text().isdigit():
            QMessageBox.critical(self, "Error", "ID Trasportatore non valido.")
            return False
        try:
            datetime.strptime(self.editDataPresa.text(), '%d/%m/%Y')
        except ValueError:
            QMessageBox.critical(self, "Error", "Data Presa in Carico non valida. Usa il formato gg/mm/aaaa.")
            return False
        try:
            datetime.strptime(self.editDataCompilazione.text(), '%d/%m/%Y')
        except ValueError:
            QMessageBox.critical(self, "Error", "Data Compilazione non valida. Usa il formato gg/mm/aaaa.")
            return False
        return True

    def addDetail(self):
        self.add_details = CrudDettaglioCmr(self.cmr_id)
        print(f'cmr_id: {self.cmr_id}')
        self.add_details.show()

    def get_cmr_id(self):
        # Questo metodo restituisce il cmr_id corrente
        return self.cmr_id

    # def stampa_cmr(parent, cmr_id):
    #     # Percorso al file .jasper
    #     report_file = "C:/Users/stefano.LVZZ/JaspersoftWorkspace/MyReports/CMR.jasper"
    #     # Directory in cui verrà generato il PDF
    #     output_dir = "C:/Users/stefano.LVZZ/Desktop/"
    #     output_pdf = os.path.join(output_dir, "CMR.pdf")
    #     db_path = "C:/Users/stefano.LVZZ/PycharmProjects/cmrProject/app.db"
    #     jdbc_dir = "C:/Users/stefano.LVZZ/PycharmProjects/cmrProject/drivers"
    #
    #     # Comando per eseguire JasperStarter
    #     command = [
    #         "java",
    #         "-Djava.ext.dirs=" + jdbc_dir,  # Specifica la directory dei driver JDBC
    #         "-jar", "C:/Program Files (x86)/JasperStarter/lib/jasperstarter.jar",
    #         "pr", report_file,
    #         "-f", "pdf",
    #         "-o", output_dir,
    #         "-t", "generic",
    #         "--db-driver", "org.sqlite.JDBC",
    #         "--db-url", f"jdbc:sqlite:{db_path}",
    #         "-P", f"cmr_id={cmr_id}"  # Passa il parametro cmr_id
    #
    #     ]
    #
    #     # # con parametro
    #     # command = [
    #     #     '"C:/Program Files (x86)/JasperStarter/bin/jasperstarter"',
    #     #     "pr", report_file,
    #     #     "-f", "pdf",
    #     #     "-o", output_dir,
    #     #     "-t", "generic",
    #     #     "--db-driver", "org.sqlite.JDBC",
    #     #     "--db-url", f"jdbc:sqlite:{db_path}",
    #     #     "-P", f"cmr_id={cmr_id}"  # Passa il parametro cmr_id
    #     # ]
    #     print(f"Running command: {' '.join(command)}")
    #
    #     # Esecuzione del comando
    #     result = subprocess.run(command, capture_output=True, text=True)
    #
    #     print(f"Return code: {result.returncode}")
    #     print(f"Stdout: {result.stdout}")
    #     print(f"Stderr: {result.stderr}")
    #
    #     # Verifica l'output del comando
    #     if result.returncode == 0:
    #         QMessageBox.information(parent, "Successo", "Report generato con successo!")
    #         # Apri il PDF generato
    #         print(f"output_pdf: {output_pdf}")
    #         parent.open_pdf(output_pdf)
    #     else:
    #         QMessageBox.critical(parent, "Errore", f"Errore nella generazione del report:\n{result.stderr}")

    def stampa_cmr(parent, cmr_id):
        # Percorso al file .jasper

        # Costruisci il percorso relativo al file .jasper
        report_file = os.path.join(PROJECT_DIR, "reports", "cmr.jasper")

        # report_file = "C:/Users/stefano.LVZZ/JaspersoftWorkspace/MyReports/CMR.jasper"
        # Directory in cui verrà generato il PDF
        output_dir = "C:/Users/stefano.LVZZ/Desktop/"
        output_pdf = os.path.join(output_dir, "cmr.pdf")
        db_path = "C:/Users/stefano.LVZZ/PycharmProjects/cmrProject/app.db"
        driver_path = "C:/Users/stefano.LVZZ/PycharmProjects/cmrProject/drivers/sqlite-jdbc-3.46.0.0.jar"

        print(f"output_dir: {output_dir}")

        # Comando aggiornato per eseguire JasperStarter con -classpath
        command = [
            'C:/Program Files (x86)/Java/jre1.8.0_421/bin/java',  # Percorso al binario di Java 8
            "-classpath", driver_path + ";C:/Program Files (x86)/JasperStarter/lib/jasperstarter.jar",
            "de.cenote.jasperstarter.App",
            "pr", report_file,
            "-f", "pdf",
            "-o", output_dir,
            "-t", "generic",
            "--db-driver", "org.sqlite.JDBC",
            "--db-url", f"jdbc:sqlite:{db_path}",
            "-P", f"cmr_id={cmr_id}"
        ]

        print(f"Running command: {' '.join(command)}")

        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")

        # Verifica l'output del comando
        if result.returncode == 0:
            QMessageBox.information(parent, "Successo", "Report generato con successo!")
            # Apri il PDF generato
            parent.open_pdf(output_pdf)
        else:
            QMessageBox.critical(parent, "Errore", f"Errore nella generazione del report:\n{result.stderr}")

    def open_pdf(self, pdf_path):
        # Apri il PDF con l'applicazione di default del sistema operativo
        if os.path.exists(pdf_path):
            if sys.platform == "win32":
                os.startfile(pdf_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", pdf_path])
            else:
                subprocess.call(["xdg-open", pdf_path])
        else:
            QMessageBox.warning(self, "Errore", f"Il file {pdf_path} non esiste.")