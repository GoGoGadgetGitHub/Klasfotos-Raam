from UI import Ui_RaamSettings
from shared.commen import *
from shared.paths import *
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QPixmap, QImage
from PIL import ImageDraw, ImageFont, Image
from logging import disable, warning, critical, info

class RaamSettings(Ui_RaamSettings, QDialog):
    def __init__(self, MainWindow) -> None:
        super().__init__()
        self.setupUi(self)
        
        self.imgPreview.setScaledContents(True)
        self.fontColour = (0,0,0)
        self.MainWindow = MainWindow
        self.rTemplate = MainWindow.templatePathR
        
        self.rbtBalck.setChecked(True)
        self.display_preview()
        
        self.rbtBalck.clicked.connect(self.setColour)
        self.rbtWhite.clicked.connect(self.setColour)
        self.btnConfirm.clicked.connect(self.confirm)
      
    def confirm(self):
        self.postSettings()
        if self.MainWindow.cbxKlas.isChecked():
            from .klasfotoSettings_cls import KlasfotoSettings
            self.KlasfotoSettings = KlasfotoSettings(self.MainWindow)
            self.hide()
            self.KlasfotoSettings.show()
        else:
            self.hide()
            self.MainWindow.run()
        
    def setColour(self):
        if self.rbtBalck.isChecked():
            self.fontColour = (0,0,0)
        if self.rbtWhite.isChecked():
            self.fontColour = (255,255,255)
        self.display_preview()
    
    def postSettings(self):
        self.MainWindow.rColour = self.fontColour
        
    def display_preview(self):
        image = Image.open(self.MainWindow.templatePathR)
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 40)
        
        t_PosX = 10
        t_PosY = 7.85*300
        
        draw.text((t_PosX,t_PosY), "SAMPLE", self.fontColour, font = font)
        
        image2 = image.convert("RGBA")
        data = image2.tobytes("raw", "BGRA")
        qim = QImage(data, image.width, image.height, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        self.imgPreview.setPixmap(pixmap)
