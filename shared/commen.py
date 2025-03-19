from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QIcon
from .paths import LOGO

def Icon_Title(window, title):
        window.setWindowIcon(QIcon(LOGO))
        window.setWindowTitle(title)

def show_dialog_ok(title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Information)
        msgBox.setText(message)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        msgBox.exec()

def show_dialog_y_n(title, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Icon.Question)
        ret = msgBox.question(msgBox, title, message, QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        if ret == QMessageBox.StandardButton.Yes:
                return True
        return False

