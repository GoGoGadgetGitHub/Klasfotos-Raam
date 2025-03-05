from shared.commen import Icon_Title
from PyQt6.QtWidgets import QApplication
import sys
from classes import Verweking
from shared.paths import STYLE

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    
    v = Verweking()
    Icon_Title(v,"Verwerking")
    
    v.show()
    app.exit(app.exec())

if __name__ == "__main__":
        main()