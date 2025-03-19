from PIL import Image
from logging import info, warning, critical

class c_image:
    def __init__(self, path, position = (0,0)):
        self.path = path
        self.position = position
        try:
            self.image = Image.open(self.path)
        except Exception as e:
            warning(e)

    def move(self, x, y):
        self.position = (x,y)

    def show(self):
        self.image.show()
