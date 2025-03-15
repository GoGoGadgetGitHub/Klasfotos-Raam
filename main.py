from shared.commen import Icon_Title
from PyQt6.QtWidgets import QApplication
import sys
from classes import Verweking
from qt_material import apply_stylesheet

def main():
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')
    
    v = Verweking()
    Icon_Title(v,"Verwerking")
    
    v.show()
    app.exit(app.exec())

if __name__ == "__main__":
        main()