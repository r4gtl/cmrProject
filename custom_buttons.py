from PyQt5.QtWidgets import QPushButton, QToolBar, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from db.models import Cmr

class SearchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon('icons/loupe.png'))  # Imposta l'icona del pulsante
        self.setIconSize(self.sizeHint())  # Imposta la dimensione dell'icona in base al sizeHint del pulsante
        self.setFixedSize(40, 40)  # Imposta la dimensione fissa del pulsante (esempio: 40x40)

class AddButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon('icons/add-list.png'))  # Imposta l'icona del pulsante
        self.setIconSize(self.sizeHint())  # Imposta la dimensione dell'icona in base al sizeHint del pulsante
        self.setFixedSize(40, 40)  # Imposta la dimensione fissa del pulsante (esempio: 40x40)


def setup_toolbar(parent):
    tb = QToolBar("Tool Bar", parent)
    tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    addSave = QAction(QIcon('icons/save.png'), "Salva", parent)
    addSave.triggered.connect(parent.addSave)
    tb.addAction(addSave)
    # addSave.triggered.connect(parent.func_add_save)

    deleteCmr = QAction(QIcon('icons/delete-folder.png'), "Elimina", parent)
    tb.addAction(deleteCmr)
    # deleteCmr.triggered.connect(parent.func_delete_cmr)

    exitAction = QAction(QIcon('icons/exit.png'), "Esci", parent)
    exitAction.triggered.connect(parent.close)
    # tb.addAction(exitAction)

    return tb



def addSave(parent):
    # Implementazione per il pulsante "Salva"
    print("Arrivato qui! Salvataggio!")
    if parent.validateCmrData():
        # Esempio di salvataggio dei dati del CMR
        cmr_data = {
            'utente_id': parent.editUtenteId.text(),  # Esempio: recupera dati da campi della UI
            'destinatario_id': parent.editDestinatarioId.text(),
            'destinazione_id': parent.editDestinazioneId.text(),
            'luogo_presa_in_carico': parent.editLuogoPresa.text(),
            'data_presa_in_carico': parent.editDataPresa.text(),
            'documenti_allegati': parent.editDocumenti.text(),
            'istruzioni_mittente': parent.editIstruzioniMittente.text(),
            'porto_franco': parent.checkPortoFranco.text(),
            'porto_assegnato': parent.checkPortoAssegnato.text(),
            'rimborso': parent.editRimborso.text(),
            'trasportatore_id': parent.editTrasportatoreId.text(),
            'osservazioni_trasporto': parent.editOsservazioni.text(),
            'convenzioni': parent.editConvenzioni.text(),
            'compilato_a': parent.editLuogoCompilazione.text(),
            'data_compilazione': parent.editDataCompilazione.text()
            #'created_at': parent.editDestinazioneId.text(),


        }
        new_cmr = Cmr(**cmr_data)

        if new_cmr.save_cmr_data():
            QMessageBox.information(parent, "Salva", "Dati CMR salvati con successo!")
            parent.close()
        else:
            QMessageBox.warning(parent, "Errore", "Errore durante il salvataggio dei dati del CMR.")

def custom_delete_cmr(parent):
    # Implementazione per il pulsante "Elimina"
    if parent.cmr_id:
        reply = QMessageBox.question(parent, 'Elimina', 'Sei sicuro di voler eliminare questo CMR?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Esempio di eliminazione del CMR
            print(f"Eliminazione CMR {parent.cmr_id}")
            QMessageBox.information(parent, "Elimina", "CMR eliminato con successo!")
            parent.close()
    else:
        QMessageBox.warning(parent, "Elimina", "Nessun CMR da eliminare!")