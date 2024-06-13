from PyQt5.QtWidgets import QApplication

def center(window):
    frame_geometry = window.frameGeometry()
    screen_center = QApplication.desktop().availableGeometry().center()
    frame_geometry.moveCenter(screen_center)
    window.move(frame_geometry.topLeft())


def set_focus_to_widget(widget):
    widget.setFocus()