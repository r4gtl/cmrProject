from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

class SearchButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QIcon('icons/loupe.png'))  # Imposta l'icona del pulsante
        self.setIconSize(self.sizeHint())  # Imposta la dimensione dell'icona in base al sizeHint del pulsante
        self.setFixedSize(40, 40)  # Imposta la dimensione fissa del pulsante (esempio: 40x40)
