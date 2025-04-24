from PIL import Image, ImageDraw, ImageFont
from .image import c_image
from os import getcwd, listdir, path, walk, sep
from shared.paths import *

class ContactSheet:
    def __init__(self, sWidth, sHeight, folder, templatePath, GraadGrade, color, ppi = 300, minimumPadding = 10, iHeight = 5, iWidth = 8) -> None:
        self.GraadGrade = GraadGrade
        self.minimumPadding = minimumPadding
        self.folderpath = folder
        self.ppi = ppi
        self.fontColor = color
        self.sHeight = int(sHeight * ppi)
        self.sWidth = int(sWidth * ppi)
        self.iHeight = int(iHeight * ppi)
        self.iWidth = int(iWidth * ppi)
        self.origen = (0,0)
        self.paths = [path.join(r,f) for r, sd, fs in walk(folder) for f in fs if ".jpg" in f or ".JPG" in f]
        self.imageCount = len(self.paths)
        self.postioning = []
        self.width, self.height = 0, 0
        self.calc_size()
        self.yPad = self.calc_yPad()
        self.xPad = self.calc_xPad()
        self.compinsate_for_minimum_padding()
        self.clac_positioning()
        self.images = [c_image(self.paths[i] ,self.postioning[i]) for i in range(self.imageCount)]
        self.complete = Image.open(templatePath)
        self.centre()
        self.make()
        
    #Uses pillow to make an empty png with the length and width specified and procedes to place images
    #on it according to calculations
    def make(self):
        for i in self.images:
            resized = i.image.resize((self.width, self.height))
            self.complete.paste(resized, i.position)
        self.insert_text()
        
    def insert_text(self):
        """Insert graad or grade text on the image.
            This function is safe to call outside of the class.
        """
        if self.GraadGrade != "":
            text = self.GraadGrade + " " + self.folderpath.split(sep)[-1]
        else:
            text = self.folderpath.split(sep)[-1]
        
        print(text)
                 
        t_PosX = self.iWidth // 2
        t_PosY = self.iHeight
        draw = ImageDraw.Draw(self.complete)
        font = ImageFont.truetype(path.join(ASSETS,"fonts","Baskerville WGL4 BT Roman.ttf"), 115)
        
        draw.text((t_PosX,t_PosY), text, self.fontColor, font = font, anchor= "md")
    
    def save(self, name):
        """
        Calls PIL.Image.Save

        Args:
            name (str): filename of the new image
        """
        self.complete.save(name, quality = 100)

    def compinsate_for_minimum_padding(self):
        """
        If the padding is equal to zero, the width must be redused my some minimum and the padding increased by said minimum
        """
        if self.xPad == self.minimumPadding:
            self.width -= self.minimumPadding
            self.height = round(self.width * (3/2))
            self.yPad = self.calc_yPad()
            self.xPad = self.calc_xPad()
        elif self.yPad == self.minimumPadding:
            self.height -= self.minimumPadding
            self.width = round(self.height* (2/3))
            self.xPad = self.calc_xPad()

    def calc_rows(self):
        if int(self.sHeight/self.height) == 0:
            return 1
        return int(self.sHeight/self.height)

    def calc_cols(self):
        if int(self.sWidth/self.width) == 0:
            return 2
        return int(self.sWidth/self.width)

    def calc_xPad(self):
        xRemSpace = self.sWidth - (self.width * self.cols)
        xPad = xRemSpace / (self.cols-1)
        if xPad < self.minimumPadding:
            xPad = self.minimumPadding
        return (round(xPad))
    
    def calc_yPad(self):
        yRemSpace = self.sHeight - (self.height * self.rows)
        yPad = yRemSpace / (self.rows+1)
        if yPad < self.minimumPadding:
            yPad = self.minimumPadding
        return (round(yPad))

    def clac_positioning(self):
        """
        Calculates positioning of images on sheet based of rows and cols
        """
        imagesInBottom = (self.imageCount) -((self.rows-1) * self.cols)
        self.origen = (((self.iWidth - self.sWidth)//2), (self.yPad + 62 + ((self.iHeight - self.sHeight)//2))) # 60 just moves the whole sheet down a bit for aesthetic purposes
        
        #If there are less than 4 images in the bottom row
        if imagesInBottom < 4 and not self.cols == imagesInBottom:
            #And the amount of images is greater than 20
            if self.imageCount > 20:
                #Keep adding rows-1 amount of images to the bottom row until there are at least 4 and adjust the xPad accordingly
                while ((self.imageCount) -((self.rows-1) * self.cols)) < 4:
                    self.cols -= 1
                    self.xPad = self.calc_xPad()
            #And the amount of images is less than or equal to 19
            else:
                #Keep adding rows-1 amount of images to the bottom row until there are at least 3 adjust the xPad accordingly
                while ((self.imageCount) -((self.rows-1) * self.cols)) < 3:
                    self.cols -= 1
                    self.xPad = self.calc_xPad()
            
            x, y = self.origen
            for i in range(self.imageCount):
                if i == 0:
                    x = self.origen[0]
                    y = self.origen[1]
                elif i % self.cols == 0:
                    x = self.origen[0]
                    y += self.height + self.yPad
                else:
                    x += self.width + self.xPad
                self.postioning.append((x,y))
        else:
            for i in range(self.imageCount):
                if i == 0:
                    x = self.origen[0]
                    y = self.origen[1]
                elif i % self.cols == 0:
                    x = self.origen[0]
                    y += self.height + self.yPad
                else:
                    x += self.width + self.xPad
                self.postioning.append((x,y))

    def centre(self):
        """
        If the bottom row is incomplete, it will be centred so that the area to the left of the row is equal to the area to the right
        """
        if self.rows * self.cols > self.imageCount:
            index = (self.rows-1) * self.cols  #Index of first image on bottom row
            y = self.images[index].position[1] #Y pos of image
            for i in range(index, self.imageCount): 
                if i == index:
                    imagesInBottomRow = self.imageCount - ((self.rows-1) * self.cols)
                    totalXPad = self.xPad * (imagesInBottomRow - 1)
                    xUsedByImages = self.width * imagesInBottomRow
                    used = totalXPad + xUsedByImages
                    RemSpace = self.iWidth - used
                    x = RemSpace // 2
                else:
                    x += self.width + self.xPad
                self.images[i].move(x,y)

    
    def calc_size(self):
        """
        Calculates size of each image by stating with a maximum height, then slowly decreasing it until enough rows and columns can be formed to fit all images.
        """
        self.height = self.sHeight
        self.width = self.height * (2/3) # The aspect ratio is located here
        self.rows, self.cols = 1, 1
        while self.rows * self.cols < self.imageCount:   
            self.height -= 1                             
            self.width = int(self.height * (2/3))        
            self.rows = self.calc_rows()                 
            self.cols = self.calc_cols()                 