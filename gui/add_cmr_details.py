from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal
from utils import center, set_focus_to_widget
from sqlalchemy.exc import IntegrityError
from db.models import SessionLocal, Destinatario, DettaglioCmr, Cmr



class CrudDettaglioCmr(QMainWindow):
    aboutToClose = pyqtSignal()  # Segnale personalizzato

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aggiungi riga dettaglio")
        self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(300,150,500,300)
        self.setFixedSize(self.size())
        self.session = SessionLocal()
        center(self)
        self.central_widget = QWidget()  # Creazione del widget centrale
        self.setCentralWidget(self.central_widget)  # Impostazione del widget centrale
        self.UI()

        #self.show()


    def UI(self):
        self.widgets()
        self.layouts()
        self.toolBar()
        set_focus_to_widget(self.editRagioneSociale)

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
        self.delete.triggered.connect(self.delete_dettaglio)
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
        self.edit_cmr_id.hide()

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
        self.mainLayout = QVBoxLayout(self.central_widget)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.lblId, self.editId, self.edit_cmr_id)
        self.formLayout.addRow(self.lblUMisura, self.editUMisura)
        self.formLayout.addRow(self.lblNColli, self.editNColli)
        self.formLayout.addRow(self.lblImballaggio, self.editImballaggio)
        self.formLayout.addRow(self.lblDenominazione, self.editDenominazione)
        self.formLayout.addRow(self.lblStatistica, self.editStatistica)
        self.formLayout.addRow(self.lblPesoLordo, self.editPesoLordo)
        self.formLayout.addRow(self.lblVolume, self.editVolume)

        self.mainLayout.addLayout(self.formLayout)

    def save_dettaglio(self):
        # Salvataggio o aggiornamento del destinatario
        id = self.editId.text()
        ragione_sociale = self.editRagioneSociale.text()
        indirizzo_1 = self.editIndirizzo1.text()
        indirizzo_2 = self.editIndirizzo2.text()



        # Se l'ID è vuoto, creiamo un nuovo destinatario
        if not id:
            new_destinatario = Destinatario(ragione_sociale=ragione_sociale, indirizzo_1=indirizzo_1,
                                            indirizzo_2=indirizzo_2,)
                                            #created_at=datetime.date.today())
            self.session.add(new_destinatario)
            self.session.commit()
            self.editId.setText(str(new_destinatario.id))  # Mostra l'ID appena creato
            QMessageBox.information(self, "Info", "Destinatario aggiunto correttamente!")

        else:
            # Altrimenti, aggiorniamo il destinatario esistente
            destinatario = self.session.query(Destinatario).filter_by(id=id).first()
            if destinatario:
                destinatario.ragione_sociale = ragione_sociale
                destinatario.indirizzo_1 = indirizzo_1
                destinatario.indirizzo_2 = indirizzo_2
                self.session.commit()
                QMessageBox.information(self, "Info", "Destinatario modificato correttamente!")

        self.session.close()
        self.close()

    def delete_destinatario(self):
        id = self.editId.text()
        if id:
            # Mostra un messaggio di conferma
            reply = QMessageBox.question(self, 'Conferma di cancellazione',
                                         'Sei sicuro di voler eliminare questo destinatario?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Trova il destinatario da eliminare
                destinatario = self.session.query(Destinatario).filter_by(id=id).first()
                if destinatario:
                    self.session.delete(destinatario)
                    self.session.commit()
                    self.clear_fields()
            self.session.close()
            self.close()

    def clear_fields(self):
        self.editId.clear()
        self.editRagioneSociale.clear()
        self.editIndirizzo1.clear()
        self.editIndirizzo2.clear()

    def load_data(self, destinatario):
        self.editId.setText(str(destinatario.id))
        self.editRagioneSociale.setText(destinatario.ragione_sociale)
        self.editIndirizzo1.setText(destinatario.indirizzo_1)
        self.editIndirizzo2.setText(destinatario.indirizzo_2)

    def closeEvent(self, event):
        self.aboutToClose.emit()  # Emette il segnale aboutToClose quando la finestra sta per chiudersi
        event.accept()


