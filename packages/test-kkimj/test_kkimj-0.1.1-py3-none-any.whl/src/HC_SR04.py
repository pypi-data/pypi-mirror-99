from serial import Serial

class testerkkimj:
    def test(self):
        print("Test is done")

class HC_SR04:
    def __init__(self, channel = 1, direction = "left", port = '/dev/ttyUSB0'):
        self.channel = channel
        self.port = port
        self.direction = direction
    
    def setSerialPort(self, port):
        self.port = port

    def OpenSerial(self):
        self.serial =  Serial(self.port, 115200, timeout = 3)
    
    def CloseSerial(self):
        self.serial.close()

    def getData(self, separator=' '):
        return list(map(int, self.serial.readline().decode('utf-8').strip().split(separator)))

    def Test(self):
        print('Test method of HC_SR04 Class')
        if self:
            if self.port:
                print('Port : %s'%(self.port))
            if self.channel:
                print('Channel : %s'%(self.channel))
            if self.direction:
                print('Direction : %s'%(self.port))

class HC_SR04_fair:
    pass
