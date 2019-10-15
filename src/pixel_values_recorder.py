import PIL
from PIL import ImageGrab
import numpy as np


class PixelValueRecorder:
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

    def getPixelsArray(self, x, y, widht, height):
        tempArray = np.empty((widht, height, 3))
        for w in range(widht):
            for h in range(height):
                tempArray[w, h] = self.getPixel(x + w, y + h)
        # print(tempArray)
        return tempArray
