from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtCore import Qt, pyqtSignal


class SearchDialog(QDialog):
    item_selected = pyqtSignal(int)

    def __init__(self, items, headers, search_field):
        super().__init__()
        self.items = items
        self.headers = headers
        self.search_field = search_field

        # Verifica che search_field sia presente in headers
        if self.search_field not in self.headers:
            raise ValueError(f"Search field '{self.search_field}' is not in headers {self.headers}")

        self.setWindowTitle("Finestra di Ricerca")
        self.resize(600, 400)
        self.UI()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.filterLineEdit = QLineEdit()
        self.filterLineEdit.setPlaceholderText(f"Filtra per {self.search_field}")
        self.filterLineEdit.textChanged.connect(self.filter_table)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellDoubleClicked.connect(self.emit_selected_item)
        self.populate_table()

    def layouts(self):
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.filterLineEdit)
        self.layout.addWidget(self.table)

    def populate_table(self):
        self.table.setRowCount(len(self.items))
        for row, item in enumerate(self.items):
            for column, header in enumerate(self.headers):
                self.table.setItem(row, column, QTableWidgetItem(str(item[column])))

    def filter_table(self):
        filter_text = self.filterLineEdit.text().lower()
        print(f"Filter text: {filter_text}")
        search_column_index = self.headers.index(self.search_field)
        for row in range(self.table.rowCount()):
            try:
                cell_item = self.table.item(row, search_column_index)
                if cell_item is not None:
                    cell_text = cell_item.text().lower()
                    print(f"Row {row}, Cell text: {cell_text}")
                    self.table.setRowHidden(row, filter_text not in cell_text)
                else:
                    print(f"Row {row}, Cell item is None")
                    self.table.setRowHidden(row, True)
            except Exception as e:
                print(f"Error at row {row}: {e}")
                self.table.setRowHidden(row, True)

    def emit_selected_item(self, row, column):
        try:
            item_id = int(self.table.item(row, 0).text())
            print(f"Selected item ID: {item_id}")
            self.item_selected.emit(item_id)
            self.accept()
        except Exception as e:
            print(f"Error while emitting signal: {e}")
