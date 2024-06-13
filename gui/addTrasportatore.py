from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSignal
from utils import center, set_focus_to_widget
from sqlalchemy.exc import IntegrityError
from db.models import SessionLocal, Trasportatore



class CrudTrasportatore(QMainWindow):
    aboutToClose = pyqtSignal()  # Segnale personalizzato

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CMR Manager")
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
        # New CMR
        self.addSave = QAction(QIcon('icons/save.png'), "Salva", self)
        self.tb.addAction(self.addSave)
        self.addSave.triggered.connect(self.save_trasportatore)
        self.tb.addSeparator()
        self.delete = QAction(QIcon('icons/delete-folder.png'), "Elimina", self)
        self.tb.addAction(self.delete)
        self.delete.triggered.connect(self.delete_trasportatore)
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

        self.lblRagioneSociale = QLabel("Ragione Sociale:")
        self.editRagioneSociale = QLineEdit()

        self.lblIndirizzo1 = QLabel("Indirizzo 1:")
        self.editIndirizzo1 = QLineEdit()

        self.lblIndirizzo2 = QLabel("Indirizzo 2:")
        self.editIndirizzo2 = QLineEdit()

    def layouts(self):
        self.mainLayout = QVBoxLayout(self.central_widget)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.lblId, self.editId)
        self.formLayout.addRow(self.lblRagioneSociale, self.editRagioneSociale)
        self.formLayout.addRow(self.lblIndirizzo1, self.editIndirizzo1)
        self.formLayout.addRow(self.lblIndirizzo2, self.editIndirizzo2)

        self.mainLayout.addLayout(self.formLayout)

    def save_trasportatore(self):
        # Salvataggio o aggiornamento del trasportatore
        id = self.editId.text()
        ragione_sociale = self.editRagioneSociale.text()
        indirizzo_1 = self.editIndirizzo1.text()
        indirizzo_2 = self.editIndirizzo2.text()



        # Se l'ID è vuoto, creiamo un nuovo trasportatore
        if not id:
            new_trasportatore = Trasportatore(ragione_sociale=ragione_sociale, indirizzo_1=indirizzo_1,
                                            indirizzo_2=indirizzo_2,)
                                            #created_at=datetime.date.today())
            self.session.add(new_trasportatore)
            self.session.commit()
            self.editId.setText(str(new_trasportatore.id))  # Mostra l'ID appena creato
            QMessageBox.information(self, "Info", "Trasportatore aggiunto correttamente!")

        else:
            # Altrimenti, aggiorniamo il destinatario esistente
            trasportatore = self.session.query(Trasportatore).filter_by(id=id).first()
            if trasportatore:
                trasportatore.ragione_sociale = ragione_sociale
                trasportatore.indirizzo_1 = indirizzo_1
                trasportatore.indirizzo_2 = indirizzo_2
                self.session.commit()
                QMessageBox.information(self, "Info", "Trasportatore modificato correttamente!")

        self.session.close()
        self.close()

    def delete_trasportatore(self):
        id = self.editId.text()
        if id:
            # Mostra un messaggio di conferma
            reply = QMessageBox.question(self, 'Conferma di cancellazione',
                                         'Sei sicuro di voler eliminare questo trasportatore?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Trova il trasportatore da eliminare
                trasportatore = self.session.query(Trasportatore).filter_by(id=id).first()
                if trasportatore:
                    self.session.delete(trasportatore)
                    self.session.commit()
                    self.clear_fields()
            self.session.close()

            self.close()

    def clear_fields(self):
        self.editId.clear()
        self.editRagioneSociale.clear()
        self.editIndirizzo1.clear()
        self.editIndirizzo2.clear()

    def load_data(self, trasportatore):
        self.editId.setText(str(trasportatore.id))
        self.editRagioneSociale.setText(trasportatore.ragione_sociale)
        self.editIndirizzo1.setText(trasportatore.indirizzo_1)
        self.editIndirizzo2.setText(trasportatore.indirizzo_2)

    def closeEvent(self, event):
        self.aboutToClose.emit()  # Emette il segnale aboutToClose quando la finestra sta per chiudersi
        self.clear_fields()
        event.accept()

