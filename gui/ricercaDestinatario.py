from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView


class RicercaDestinatario(QDialog):
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
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)

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
