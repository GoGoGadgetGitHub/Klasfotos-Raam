from UI import Ui_KlasfotoSettings
from shared.commen import *
from shared.paths import *
from ..Helper_Classes import ContactSheet
from PIL import Image, ImageDraw, ImageFont, ImageQt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QCheckBox
from PyQt6.QtCore import QThreadPool
import logging
from logging import disable, warning, critical, info
from os import listdir
from os.path import join
    
class KlasfotoSettings(Ui_KlasfotoSettings, QDialog):
    def __init__(self, mainwondow):
        super().__init__()
        #logging.getLogger().addHandler(logging.StreamHandler())
        self.setupUi(self)
        self.imgPreview.setScaledContents(True)
        self.mainwindow = mainwondow
        self.settings = {}
        self.classes =  [file for file in listdir(join(mainwondow.Folder,"ORG"))]
        self.currentClass = self.classes[0]
        self.rows = len(self.classes)
        self.fontColour = (255,255,255)
        self.rbtWhite.setChecked(True)
         
        
        #Initial Table Setup
        for row in range(self.rows):
            self.tblSettings.insertRow(self.tblSettings.rowCount())
            self.tblSettings.setItem(row,0, QTableWidgetItem(f"{self.classes[row]}"))
            self.settings[self.classes[row]] = None
            for col in range(1,4):
                self.tblSettings.setCellWidget(row,col, QCheckBox(self.tblSettings))
                cb = self.tblSettings.cellWidget(row,col)
                cb.clicked.connect(self.cbClicked)
        self.GraadGradeNone = ""
        self.cbxAllNone.setChecked(True)
        self.allNone()
                
        self.cbxAllGraad.clicked.connect(self.allGraad)
        self.cbxAllGrade.clicked.connect(self.allGrade)
        self.cbxAllNone.clicked.connect(self.allNone)
        self.tblSettings.clicked.connect(self.displayPreview)
        self.rbtBlack.clicked.connect(self.setColour)
        self.rbtWhite.clicked.connect(self.setColour)
        self.btnConfirm.clicked.connect(self.confirm)
    
    def confirm(self):
        self.postSettings()
        self.hide()
        self.mainwindow.run()
        
    def setColour(self):
        if self.rbtWhite.isChecked():
            self.fontColour = (255,255,255)
        if self.rbtBlack.isChecked():
            self.fontColour = (0,0,0)
        self.displayPreview()
    
    def setGraadGrandeNone(self):
        row = self.tblSettings.currentIndex().row()
        self.currentClass = self.classes[row]
        if row != -1:
            if self.tblSettings.cellWidget(row,1).isChecked():
                self.GraadGradeNone = "Graad"
            if self.tblSettings.cellWidget(row,2).isChecked():
                self.GraadGradeNone = "Grade"
            if self.tblSettings.cellWidget(row,3).isChecked():
                self.GraadGradeNone = ""
        
    def displayPreview(self):
        self.setGraadGrandeNone()
        image = Image.open(self.mainwindow.templatePathK)
        info("Image loaded")
        if self.GraadGradeNone == "":
            text = self.currentClass
        else:
            text = self.GraadGradeNone + " " + self.currentClass
        
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(join(ASSETS, "fonts", "Baskerville WGL4 BT Roman.ttf"), 115)
        
        t_PosX = (8 * 300) // 2
        t_PosY = (5 * 300)
        
        draw.text((t_PosX,t_PosY), text, self.fontColour, font = font, anchor= "md")
        info("Text inserted")
        
        image2 = image.convert("RGBA")
        data = image2.tobytes("raw", "BGRA")
        qim = QImage(data, image.width, image.height, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(qim)
        self.imgPreview.setPixmap(pixmap)
    
    def allGraad(self):
        self.cbxAllGrade.setChecked(False)
        self.cbxAllNone.setChecked(False)
        for y in range(self.rows):
            box = [self.tblSettings.cellWidget(y,1), self.tblSettings.cellWidget(y,2), self.tblSettings.cellWidget(y,3)]
            box[0].setChecked(self.cbxAllGraad.isChecked())
            box[1].setChecked(False)
            box[2].setChecked(False)
        self.displayPreview()
            
    def allGrade(self):
        self.cbxAllGraad.setChecked(False)
        self.cbxAllNone.setChecked(False)
        for y in range(self.rows):
            box = [self.tblSettings.cellWidget(y,1), self.tblSettings.cellWidget(y,2), self.tblSettings.cellWidget(y,3)]
            box[0].setChecked(False)
            box[1].setChecked(self.cbxAllGrade.isChecked())
            box[2].setChecked(False)
        self.displayPreview()
                    
    def allNone(self):
        self.cbxAllGrade.setChecked(False)
        self.cbxAllGraad.setChecked(False)
        for y in range(self.rows):
            box = [self.tblSettings.cellWidget(y,1), self.tblSettings.cellWidget(y,2), self.tblSettings.cellWidget(y,3)]
            box[0].setChecked(False)
            box[1].setChecked(False)
            box[2].setChecked(self.cbxAllNone.isChecked())
        self.displayPreview()
            
    def cbClicked(self):
        y, x = self.tblSettings.currentRow(), self.tblSettings.currentColumn()
        if x == 1:
            self.tblSettings.cellWidget(y,2).setChecked(False)
            self.tblSettings.cellWidget(y,3).setChecked(False)
            self.GraadGradeNone = "Graad" 
        if x == 2:
            self.tblSettings.cellWidget(y,1).setChecked(False)
            self.tblSettings.cellWidget(y,3).setChecked(False)
            self.GraadGradeNone = "Grade" 
        if x == 3:
            self.tblSettings.cellWidget(y,1).setChecked(False)
            self.tblSettings.cellWidget(y,2).setChecked(False)
            self.GraadGradeNone = "" 
        self.displayPreview()
        
    def postSettings(self):
        for rowCount in range(self.rows):
            if self.tblSettings.cellWidget(rowCount,1).isChecked():
                self.settings[list(self.classes)[rowCount]] = "Graad"
            if self.tblSettings.cellWidget(rowCount,2).isChecked():
                self.settings[list(self.classes)[rowCount]] = "Grade"
            if self.tblSettings.cellWidget(rowCount,3).isChecked():
                self.settings[list(self.classes)[rowCount]] = ""
                
        self.mainwindow.klasfotoSettings = self.settings
        self.mainwindow.kColour = self.fontColour
