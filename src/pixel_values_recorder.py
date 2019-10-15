import PIL
from PIL import ImageGrab
import numpy as np


class PixelValuesRecorder:
    def __init__(self, screenWidth: int, screenHeight: int, nWidthLed: int, nHeightLed: int):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.nWidthLed = nWidthLed
        self.nHeightLed = nHeightLed
        self.screen = None

    def getPixel(self, x, y):
        return self.screen[x, y]

    def screenShot(self):
        self.screen = PIL.ImageGrab.grab().load()

    def getPixelArray(self, x: int, y: int, width: int, height: int, step=1):
        xSize = int((width + step - 1) / step)
        ySize = int((height + step - 1) / step)
        tempArray = np.empty((xSize, ySize, 3))
        for w in range(xSize):
            for h in range(ySize):
                tempArray[w, h] = self.getPixel(x + w * step, y + h * step)
        return tempArray