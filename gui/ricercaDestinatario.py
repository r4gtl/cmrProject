from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QLineEdit,
                             QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView)
from PyQt5.QtCore import Qt, pyqtSignal

class RicercaDestinatario(QDialog):
    destinatario_selected = pyqtSignal(int)
    def __init__(self, destinatari):
        super().__init__()
        self.setWindowTitle("Finestra Destinatari")

        self.destinatari = destinatari  # Lista delle istanze di Destinatario
        self.resize(600, 400)


        self.UI()






    def UI(self):
        self.widgets()
        self.layouts()



    def widgets(self):

        # Campo di testo per il filtro
        self.filterLineEdit = QLineEdit()
        self.filterLineEdit.setPlaceholderText("Filtra per ragione sociale")
        self.filterLineEdit.textChanged.connect(self.filter_table)

        # Tabella per visualizzare i dati dei destinatari
        self.table = QTableWidget()
        self.table.setColumnCount(2)  # Numero di colonne
        self.table.setHorizontalHeaderLabels(["ID", "Ragione Sociale"])
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellDoubleClicked.connect(self.emit_selected_destinatario)
        self.populate_table()


    def layouts(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.table)


    def populate_table(self):
        self.table.setRowCount(len(self.destinatari))
        for row, destinatario in enumerate(self.destinatari):
            self.table.setItem(row, 0, QTableWidgetItem(str(destinatario.id)))
            self.table.setItem(row, 1, QTableWidgetItem(destinatario.ragione_sociale))

    def filter_table(self):
        filter_text = self.filterLineEdit.text().lower()
        for row in range(self.table.rowCount()):
            ragione_sociale = self.table.item(row, 1).text().lower()
            self.table.setRowHidden(row, filter_text not in ragione_sociale)

    def emit_selected_destinatario(self, row, column):
        try:
            destinatario_id = int(self.table.item(row, 0).text())  # Ottieni l'ID dalla prima colonna
            print(f"Destinatario ID: {destinatario_id}")
            self.destinatario_selected.emit(destinatario_id)  # Emetti il segnale con l'ID del destinatario selezionato
            self.accept()  # Chiudi la finestra di dialogo
        except Exception as e:
            print(f"Errore durante l'emissione del segnale: {e}")