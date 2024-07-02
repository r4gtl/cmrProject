from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal
from utils import center, set_focus_to_widget
from sqlalchemy.exc import IntegrityError
from db.models import SessionLocal, Destinatario, DettaglioCmr, Cmr



class CrudDettaglioCmr(QMainWindow):
    aboutToClose = pyqtSignal()  # Segnale personalizzato

    def __init__(self, cmr_id=None):
        super().__init__()
        self.setWindowTitle("Aggiungi riga dettaglio")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(600,150,500,300)
        self.setFixedSize(self.size())
        self.session = SessionLocal()
        self.cmr_id = cmr_id
        center(self)
        self.central_widget = QWidget()  # Creazione del widget centrale
        self.setCentralWidget(self.central_widget)  # Impostazione del widget centrale
        self.UI()

        #self.show()


    def UI(self):
        self.widgets()
        self.layouts()
        self.toolBar()
        self.loadCmrId()
        #set_focus_to_widget(self.editRagioneSociale)

    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        #self.layout.addWidget(self.tb)  # Aggiunta della toolbar al layout
        #self.layout.addStretch()  # Aggiunta di uno spacer per spingere il contenuto in basso

        # ToolBar Buttons
        # New Details
        self.addSave = QAction(QIcon('icons/save.png'), "Salva", self)
        self.tb.addAction(self.addSave)
        self.addSave.triggered.connect(self.save_dettaglio)
        self.tb.addSeparator()
        self.delete = QAction(QIcon('icons/delete-folder.png'), "Elimina", self)
        self.tb.addAction(self.delete)
        #self.delete.triggered.connect(self.delete_dettaglio)
        self.tb.addSeparator()
        self.exit = QAction(QIcon('icons/exit.png'), "Esci", self)
        self.exit.triggered.connect(self.close)
        self.tb.addAction(self.exit)
        # self.exit.triggered.connect(self.funcexit)
        self.tb.addSeparator()

    def widgets(self):
        self.lblId = QLabel("ID:")
        self.editId = QLineEdit()
        self.editId.setReadOnly(True)  # Impedisce la modifica dell'ID

        #self.lblRagioneSociale = QLabel("Ragione Sociale:")
        self.edit_cmr_id = QLineEdit()
        self.edit_cmr_id.setReadOnly(True)

        self.lblUMisura = QLabel("Unità di Misura:")
        self.editUMisura = QLineEdit()

        self.lblNColli = QLabel("Numero")
        self.editNColli = QLineEdit()

        self.lblImballaggio = QLabel("Imballaggio")
        self.editImballaggio = QLineEdit()

        self.lblDenominazione = QLabel("Denominazione")
        self.editDenominazione = QLineEdit()

        self.lblStatistica = QLabel("Statistica")
        self.editStatistica = QLineEdit()

        self.lblPesoLordo = QLabel("Peso Lordo (Kg)")
        self.editPesoLordo = QLineEdit()

        self.lblVolume = QLabel("Volume (Mc)")
        self.editVolume = QLineEdit()


    def layouts(self):
        self.groupForm = QGroupBox("Dati Dettaglio")
        self.mainLayout = QHBoxLayout(self.central_widget)
        # self.mainLayout = QVBoxLayout(self.groupForm)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.lblId, self.editId)
        self.formLayout.addRow(self.lblUMisura, self.editUMisura)
        self.formLayout.addRow(self.lblNColli, self.editNColli)
        self.formLayout.addRow(self.lblImballaggio, self.editImballaggio)
        self.formLayout.addRow(self.lblDenominazione, self.editDenominazione)
        self.formLayout.addRow(self.lblStatistica, self.editStatistica)
        self.formLayout.addRow(self.lblPesoLordo, self.editPesoLordo)
        self.formLayout.addRow(self.lblVolume, self.editVolume)
        self.formLayout.addRow(self.edit_cmr_id)
        self.groupForm.setLayout(self.formLayout)
        self.mainLayout.addWidget(self.groupForm)
        # self.setLayout(self.mainLayout)

    def save_dettaglio(self):
        if self.validateCmrDettaglio():
            cmr_dettaglio_data = {
                'id': int(self.editId.text()),
                'cmr_id': int(self.edit_cmr_id.text()),
                'u_misura': self.editUMisura.text(),
                'n_colli': self.editNColli.text(),
                'imballaggio': self.editImballaggio.text(),
                'denominazione': self.editDenominazione.text(),
                'statistica': self.editStatistica.text(),
                'peso_lordo_kg': int(self.editStatistica.text()),
                'volume_mc': self.editVolume.text(),
            } # Salvataggio o aggiornamento del destinatario
            new_detail = DettaglioCmr(**cmr_dettaglio_data)
            if new_detail.save_dettaglio_cmr_data():
                self.editId.setText(str(new_detail.id))
                QMessageBox.information(self, "Success", "CMR salvato con successo!")
            else:
                QMessageBox.critical(self, "Error", "Errore durante il salvataggio del CMR.")

    def delete_dettaglio(self):
        id = self.editId.text()
        if id:
            # Mostra un messaggio di conferma
            reply = QMessageBox.question(self, 'Conferma di cancellazione',
                                         'Sei sicuro di voler eliminare questo dettaglio?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Trova il destinatario da eliminare
                dettaglio = self.session.query(DettaglioCmr).filter_by(id=id).first()
                if dettaglio:
                    self.session.delete(dettaglio)
                    self.session.commit()
                    self.clear_fields()
            self.session.close()
            self.close()

    def clear_fields(self):
        self.editId.clear()
        self.edit_cmr_id.clear()
        self.editUMisura.clear()
        self.editNColli.clear()
        self.editImballaggio.clear()
        self.editDenominazione.clear()
        self.editStatistica.clear()
        self.editStatistica.clear()
        self.editVolume.clear()

    def load_data(self, destinatario):
        # self.editId.setText(str(destinatario.id))
        # self.editRagioneSociale.setText(destinatario.ragione_sociale)
        # self.editIndirizzo1.setText(destinatario.indirizzo_1)
        # self.editIndirizzo2.setText(destinatario.indirizzo_2)
        pass

    def closeEvent(self, event):
        self.aboutToClose.emit()  # Emette il segnale aboutToClose quando la finestra sta per chiudersi
        event.accept()

    def validateCmrDettaglio(self):
        if not self.editId.text().isdigit():
            QMessageBox.critical(self, "Error", "ID dettaglio non valido.")
            return False
        if not self.edit_cmr_id.text().isdigit():
            QMessageBox.critical(self, "Error", "ID CMR non valido.")
            return False
        if not self.editUMisura.text():
            QMessageBox.critical(self, "Error", "Unità di misura non valido.")
            return False
        if not self.editNColli.text():
            QMessageBox.critical(self, "Error", "Numero colli non valido.")
            return False

        return True

    def loadCmrId(self):
        if self.cmr_id:
            self.edit_cmr_id.setText(str(self.cmr_id))
            self.edit_cmr_id.setReadOnly(True)

    def generate_new_detail_id(self):
        # Query per trovare l'ID massimo attuale e incrementarlo di 1
        max_id = self.session.query(func.max(DettaglioCmr.id)).scalar() or 0
        return max_id + 1

