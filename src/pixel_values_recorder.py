import PIL
from PIL import ImageGrab
import numpy as np

from src.position import Position


class PixelValuesRecorder:

    def __init__(self, screenWidth: int, screenHeight: int, nWidthLed: int, nHeightLed: int, arrayDepth: int = 400):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.nWidthLed = nWidthLed
        self.nHeightLed = nHeightLed
        self.screen = None
        self.widthLedArrayLength = int(self.screenHeight / nWidthLed)
        self.heightLedArrayLength = int(self.screenWidth / nHeightLed)
        self.arrayDepth = arrayDepth

    def getPixel(self, x, y):
        return self.screen[x, y]

    def screenShot(self):
        self.screen = PIL.ImageGrab.grab().load()

    @staticmethod
    def getArraySize(width: int, height: int, step: int):
        xSize = int(width / step)
        ySize = int(height / step)
        return xSize, ySize

    def getPixelArray(self, x: int, y: int, width: int, height: int, step=1):
        xSize, ySize = self.getArraySize(width, height, step)
        tempArray = np.empty((xSize, ySize, 3))
        for w in range(xSize):
            for h in range(ySize):
                tempArray[w, h] = self.getPixel((x + w * step), (y + h * step))
        return tempArray

    def getLedStripArray(self, position: Position, step=3):
        stripArray = None

        if position == Position.left:
            xSize, ySize = self.getArraySize(self.arrayDepth, self.widthLedArrayLength, step)
            stripArray = np.empty((self.nWidthLed, xSize, ySize, 3))
            for i in range(self.nWidthLed):
                tempArray = np.array(
                    self.getPixelArray(0, i * self.widthLedArrayLength, self.arrayDepth, self.widthLedArrayLength,
                                       step))
                stripArray[i] = np.array(tempArray)

        elif position == Position.right:
            xSize, ySize = self.getArraySize(self.arrayDepth, self.widthLedArrayLength, step)
            stripArray = np.empty((self.nWidthLed, xSize, ySize, 3))
            for i in range(self.nWidthLed):
                tempArray = np.array(
                    self.getPixelArray(self.screenWidth - self.arrayDepth - 1, i * self.widthLedArrayLength,
                                       self.arrayDepth, self.widthLedArrayLength, step))
                stripArray[i] = np.array(tempArray)

        elif position == Position.top:
            xSize, ySize = self.getArraySize(self.heightLedArrayLength, self.arrayDepth, step)
            stripArray = np.empty((self.nHeightLed, xSize, ySize, 3))
            for i in range(self.nHeightLed):
                tempArray = np.array(
                    self.getPixelArray(i * self.heightLedArrayLength, 0,
                                       self.heightLedArrayLength, self.arrayDepth, step))
                stripArray[i] = np.array(tempArray)

        elif position == Position.bottom:
            xSize, ySize = self.getArraySize(self.heightLedArrayLength, self.arrayDepth, step)
            stripArray = np.empty((self.nHeightLed, xSize, ySize, 3))
            for i in range(self.nHeightLed):
                tempArray = np.array(
                    self.getPixelArray(i * self.heightLedArrayLength, self.screenHeight - self.arrayDepth - 1,
                                       self.heightLedArrayLength, self.arrayDepth, step))
                stripArray[i] = np.array(tempArray)

        return stripArray
