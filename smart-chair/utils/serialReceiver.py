import serial


class Receiver:
    def __init__(self, port, baudrate, bytesize, timeout):
        self.data = object()
        self.serialPort = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, timeout=timeout,
                                        stopbits=serial.STOPBITS_ONE)
        self.serialString = ""

    def receiveInfo(self):
        if self.serialPort.in_waiting > 0:
            self.serialString = self.serialPort.readline()
            self.serialPort.write("Data ok!")
            return self.serialString.decode('Ascii')

    def getSerialPort(self):
        return self.serialPort

    def getData(self):
        return self.data
