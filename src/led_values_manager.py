import numpy as np

from led_values_sender import LedValuesSender
from pixel_values_recorder import PixelValuesRecorder
from position import Position


class LedValuesManager:
    def __init__(self, screenWidth: int, screenHeight: int, nWidthLed: int, nHeightLed: int, arduinoPath: str = 'COM5',
                 arrayDepth: int = 100, precision: int = 5, bitrate: int = 500000, timeout: int = 1):          
        self.pixelValuesRecorder = PixelValuesRecorder(screenWidth, screenHeight, nWidthLed, nHeightLed, arrayDepth)
        self.ledValuesSender = LedValuesSender(arduinoPath, bitrate, timeout)
        self.precision = precision
        self.isRunning = True

    @staticmethod
    def getMeanLedValue(pixelArray: np.ndarray):
        meanPixel = np.empty((3))

        tmp = np.array(pixelArray.mean(0))
        tmp = np.array((tmp.mean(0, dtype=int)))
        meanPixel[0] = tmp[0]
        meanPixel[1] = tmp[1]
        meanPixel[2] = tmp[2]
        return meanPixel

    def computeMeanStripLedValue(self, position: Position):
        meanArray = None

        if position == Position.left or position == Position.right:
            stripArray = self.pixelValuesRecorder.getLedStripArray(position, self.precision)
            meanArray = np.empty((self.pixelValuesRecorder.nWidthLed, 3), dtype=int)
            for i in range(self.pixelValuesRecorder.nWidthLed):
                tempArray = np.array(stripArray[i])
                meanArray[i] = self.getMeanLedValue(tempArray)

        if position == Position.top or position == Position.bottom:
            stripArray = self.pixelValuesRecorder.getLedStripArray(position, self.precision)
            meanArray = np.empty((self.pixelValuesRecorder.nHeightLed, 3), dtype=int)
            for i in range(self.pixelValuesRecorder.nHeightLed):
                tempArray = np.array(stripArray[i])
                meanArray[i] = self.getMeanLedValue(tempArray)

        # print(meanArray)
        return meanArray

    # TODO : @Kabroc I copy-pasted your code, and refactored it.
    def run(self):
        while self.isRunning:
            readText = self.ledValuesSender.read()
            #print(readText)
            if readText == b"\x00":
                #print("envoi")
                self.pixelValuesRecorder.screenShot()

                leftMeans = np.flip(self.computeMeanStripLedValue(Position.left), axis=0)
                topMeans = self.computeMeanStripLedValue(Position.top)
                rightMeans = self.computeMeanStripLedValue(Position.right)
                bottomMeans = np.flip(self.computeMeanStripLedValue(Position.bottom), axis=0)

                ledStringValues = self.getAllStringValues(leftMeans, topMeans, rightMeans, bottomMeans)
                self.ledValuesSender.sendLedValues(ledStringValues)

    def getAllStringValues(self, leftMeans: np.ndarray, topMeans: np.ndarray, rightMeans: np.ndarray,
                           bottomMeans: np.ndarray):
        s1 = self.getStringValues(leftMeans)
        s2 = self.getStringValues(topMeans)
        s3 = self.getStringValues(rightMeans)
        s4 = self.getStringValues(bottomMeans)
        StringValues = np.array([s1, s2, s3, s4], dtype=object)
        return StringValues

    @staticmethod
    def getPixelStringValue(r: int, g: int, b: int):
        return f"${r},{g},{b},"

    def getStringValues(self, meanLedArray: np.ndarray):
        tempString = ""
        for i in range(len(meanLedArray)):
            tempString = f"{tempString}{self.getPixelStringValue(meanLedArray[i][0], meanLedArray[i][1], meanLedArray[i][2])}"
        tempString += "$"
        return tempString
