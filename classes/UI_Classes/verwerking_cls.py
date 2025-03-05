from time import perf_counter
from UI import Ui_verwerking
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QColorDialog
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import QObject, QThread, pyqtSignal
from shared.commen import *
from shared.paths import *
from ..Helper_Classes.contact_sheet import ContactSheet
from .raamSettings_cls import RaamSettings
from .klasfotoSettings_cls import KlasfotoSettings
from PIL import Image, ImageDraw, ImageFont
from os import getcwd, listdir, makedirs, walk
from os.path import join, isdir, basename
import logging

class Worker(QtCore.QObject):
    done = pyqtSignal()
    started = pyqtSignal()
    
    def __init__(self, parent) -> None:
        super().__init__()
        self.par = parent
    
    def run(self):
        self.started.emit()
        if self.par.cbxRaam.isChecked():
            self.par.Raam()
        if self.par.cbxKlas.isChecked():
            self.par.Klasfotos()
        immediate_subdir = [name for name in listdir(self.par.Folder) if isdir(join(self.par.Folder, name))]    
        if self.par.cbxDrop.isChecked() and "RAAM" in immediate_subdir:
            self.par.Dropbox()
        elif self.par.cbxDrop.isChecked() and "RAAM" not in immediate_subdir:
            show_dialog_ok("Error", "No RAAM folder found. You have to raam before you can dropbox.")
            return
        self.done.emit()

class Verweking(QMainWindow, Ui_verwerking):
    
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        
        hide_console()
        
        logging.basicConfig(level= logging.INFO, filename=f"{getcwd()}/Log.log", format="%(levelname)s:%(filename)s:%(lineno)d:%(funcName)s: %(message)s")
        logging.info("_________NEW_________")
        
        self.fontColor =(0,0,0)
        self.templatePathK = ""
        self.templatePathR = ""
        self.templateR = None
        self.Folder = ""
        self.kColour = ()
        self.rColour = ()
        self.klasfotoSettings = {}

        self.btnSelectFolder.clicked.connect(self.select_folder)
        self.btnSelectTemplateK.clicked.connect(self.select_template_K)
        self.btnSelectTemplateR.clicked.connect(self.select_template_R)
        self.btnStart.clicked.connect(self.start)

#RAAM
#----------------------------------------------------------------------------------
    def insert_text(self, image, text):
        draw = ImageDraw.Draw(image)
        t_PosX = 20
        t_PosY = 2400 - 20
        try:
            font = ImageFont.truetype("arial.ttf", 25)
        except Exception as e:
            show_dialog_ok("Error", "Could not load font!")
            logging.critical(e)
            exit(0)
        
        draw.text((t_PosX,t_PosY), text, self.rColour, font = font, anchor = 'ls')

    def Raam(self):
        """
        Runs the raam function on all the images in self.Folder and saves them in a folder called RAAM
        with the same structure as the original folder
        """
        show_console()
        
        logging.info("Raam Start")
        template = Image.open(self.templatePathR)
        
        for r,ds,f in walk(f"{self.Folder}/ORG"):
            for d in ds:
                newDest = join(f"{self.Folder}/RAAM", d) 
                makedirs(newDest, exist_ok=True)
                for rt, dirs, fs in walk(join(r,d)):
                    for f in fs:
                        imagePath = path.join(r,d,f)
                        if ".jpg" not in imagePath:
                            logging.warning(f"Filename:{imagePath} is not a .jpg")
                            show_dialog_ok("Error", f"{imagePath} is not a .jpg")
                            break
                        framedImage = self.raam(imagePath).convert("RGB")
                        newFileName = f"{newDest}/{f}"
                        print("Saving: ", newFileName)
                        logging.info(f"Saving: {newFileName}")
                        framedImage.save(newFileName, quality = 100)

    def raam(self, imagePath):
        """
        Pastes image onto frame

        Args:
            imagePath (str): Path to image

        Returns:
            PIL.Image : Framed image
        """
        image = Image.open(imagePath)
        width = 1395 
        height = 2073
        resized = image.resize((width,height))
        base = Image.new("RGBA", ((5*300),(8*300)), (0,0,0,0))
        base.paste(resized, (((base.size[0]-width)//2),((base.size[1]-height)//2)))
        base.paste(self.templateR, (0,0), self.templateR)
        self.insert_text(base, basename(imagePath).split('.')[0])
        return base
#KLASFOTOS
#-----------------------------------------------------------------------------------
    def Klasfotos(self):
        """
        Creates a contact sheet for each subdir in self.Folder
        """
        print(self.klasfotoSettings)
        logging.info("Klasfotos Start")
        print("Starting with klasfotos.")
        
        makedirs(f"{self.Folder}/KLAS", exist_ok = True)
        for r, sd, fs in walk(f"{self.Folder}/ORG"):
            for d in sd:
                classPath = join(r,d)
                try:
                    GraadGradeNone = self.klasfotoSettings[d]
                    print(GraadGradeNone)

                    start = perf_counter()
                    sheet = ContactSheet(7.5, 3.765, classPath, self.templatePathK, GraadGradeNone, self.kColour)    
                    end = perf_counter()

                    print(f"Instantiation time: {end - start}")


                    name = f"{self.Folder}/KLAS/{d}.jpg"
                    
                    print(f"Saving: {name}")
                    logging.info(f"Saving: {name}")
                    sheet.save(f"{name}")
                    
                except Exception as e:
                    show_dialog_ok("Error", f"Could not make {d}. It will be ignored for now")
                    logging.warning(e)
                
#DROPBOX   
#-----------------------------------------------------------------------------------
    def Dropbox(self):
        """
        Makes a folder called DROPBOX with the same structure as self.Folder and saves a resized version of each image. 
        """
        logging.info("DropBox Start")
        print("Starting with Dropbox.")
        
        for r,ds,fs in walk(f"{self.Folder}/RAAM"):
            for d in ds:
                newDest = join(f"{self.Folder}/DROPBOX", d)
                makedirs(newDest, exist_ok=True)
                for rt, dirs, fls in walk(join(r,d)):
                    for f in fls:
                        image = Image.open(join(rt,f))
                        if image.width > image.height:
                            resized = image.resize((int((8*72)),int((5*72))))
                        else:
                            resized = image.resize((int((5*72)), int((8*72))))
                        
                        name = f"{newDest}/{f}"
                        
                        print(f"Saving: {name}")
                        logging.info(f"Saving: {name}")
                        resized.save(name)

# UI IMPLEMENTATION
#-----------------------------------------------------------------------------------

    def select_folder(self):
        prev = self.Folder
        self.Folder = QFileDialog.getExistingDirectory(self, "Choose School", LOC_PICTURES)
        if self.Folder == '':
            return
        elif prev != "" and self.Folder == "":
            self.Folder = prev
        Icon_Title(self, f"Verwerking - {self.Folder.split('/')[-1]}")

    def select_template_K(self):
        prev = self.templatePathK
        self.templatePathK = QFileDialog.getOpenFileName(self, "Choose Template",f"{self.Folder}")[0]
        if self.templatePathK == '':
            return
        elif self.templatePathK != '' and Image.open(self.templatePathK).size != (8*300,5*300):
            show_dialog_ok("Error", "Klasfoto template size must be 8x5 at 300 pixels per inch!")
            self.templatePathK = ""
            return
        elif prev != "" and self.templatePathK == "":
            self.templatePathK = prev
        self.imgKPreview.setPixmap(QtGui.QPixmap(self.templatePathK))
        self.imgKPreview.setScaledContents(True)
        self.btnStart.setEnabled(True)

    def select_template_R(self):
        prev = self.templatePathR
        self.templatePathR =QFileDialog.getOpenFileName(self, "Choose Template", self.Folder[:self.Folder.index(self.Folder.split('/')[-1])])[0]
        if self.templatePathR == '':
            return
        elif prev != "" and self.templatePathR == "":
            self.templatePathR = prev
        self.imgRPreview.setPixmap(QtGui.QPixmap(self.templatePathR))
        self.imgRPreview.setScaledContents(True)
        self.templateR = Image.open(self.templatePathR)
        self.btnStart.setEnabled(True)
    
    def run(self):
        self.worker = Worker(self)
        self.thrd = QThread()
        self.worker.moveToThread(self.thrd)
        self.worker.started.connect(lambda: show_dialog_ok("Info", "Your work is being processed. This may take a while.\n You can monitor the progress in the black console window."))
        self.thrd.started.connect(self.worker.run)
        self.worker.done.connect(self.thrd.quit)
        self.worker.done.connect(lambda: show_dialog_ok("Info", "Your work is done!"))
        self.worker.done.connect(self.worker.deleteLater)
        self.thrd.finished.connect(self.thrd.deleteLater)
        self.thrd.start()

    def start(self):
        show_console()
        try:
            if self.cbxRaam.isChecked():
                if self.templatePathR == "":
                    show_dialog_ok("Error", "You have to select a template for Raam.")
                    return
                self.rfs = RaamSettings(self)
                self.rfs.show()
            elif self.cbxKlas.isChecked():
                if self.templatePathK == "":
                    show_dialog_ok("Error", "You have to select a template for Klasfotos.")
                    return
                self.kfs = KlasfotoSettings(self)
                self.kfs.show()
        except Exception as e:
            show_dialog_ok("Error", "Something went horribly wrong. Please try again.")
            logging.warning(e)
            print(e)
            exit(0)
            
        
