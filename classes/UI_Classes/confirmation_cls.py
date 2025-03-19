from UI import Ui_confirmation
from PyQt6.QtWidgets import QDialog
from shared.commen import *

class Confirmation(Ui_confirmation, QDialog):
    def __init__(self, MianWindow) -> None:
        super().__init__()
        self.setupUi(self)
        
        self.MainWindow = MianWindow
        
        if MianWindow.GraadGrade != "":
            self.lblEorA.setText(MianWindow.GraadGrade)
            
        kColour = MianWindow.kColour 
        if kColour != ():
            if kColour == (0,0,0):
                self.lblKTextCol.setText("Black")
            else:
                self.lblKTextCol.setText("White")
                
        rColour = MianWindow.rColour 
        if rColour != ():
            if rColour == (0,0,0):
                self.lblRTextCol.setText("Black")
            else:
                self.lblRTextCol.setText("White")
                
        self.lblSchool.setText(MianWindow.Folder.split('/')[-1])
        
        self.btnBack.clicked.connect(self.back)
        self.btnConfirm.clicked.connect(self.confirm)
        
    '''def closeEvent(self, event):
        self.MainWindow.run()
        if self.MainWindow.cbxDrop.isChecked():
                self.MainWindow.Dropbox()'''
        
    def back(self):
        self.hide()
        if self.MainWindow.cbxRaam.isChecked() and self.MainWindow.cbxKlas.isChecked():
            from .klasfotoSettings_cls import KlasfotoSettings
            self.KlasfotoSettings = KlasfotoSettings(self.MainWindow)
            self.KlasfotoSettings.show()
        elif self.MainWindow.cbxRaam.isChecked() and not self.MainWindow.cbxKlas.isChecked():
            from .raamSettings_cls import RaamSettings
            self.RaamSettings = RaamSettings(self.MainWindow)
            self.RaamSettings.show()     
    
    def confirm(self):
        self.MainWindow.run()
        if self.MainWindow.cbxDrop.isChecked():
                self.MainWindow.Dropbox()
                # show_dialog_ok("Done!", "All Done! :)")