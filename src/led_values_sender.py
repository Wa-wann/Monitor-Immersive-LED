import serial


class LedValuesSender:
    def __init__(self, arduinoPath: str, bitrate: int = 500000, timeout: int = 1):
        self.arduinoPath = arduinoPath
        self.bitrate = bitrate
        self.timeout = timeout
        self.isDataSent = False
        self.isRunning = True

        self.portArduino = serial.Serial(arduinoPath, 500000, timeout=1)

    def sendLedValues(self, ledStringValues):
        for i in range(len(ledStringValues)):
            self.portArduino.write(str.encode(ledStringValues[i]))
            #print(ledStringValues[i])
        self.portArduino.write(str.encode('#'))

    def read(self):
        return self.portArduino.read()
        
