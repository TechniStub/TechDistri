import RPi.GPIO as gpio
import time

class DistriHandler():
    def __init__(self, SH_CP, DS, ST_CP, nChain=1, nOutput=8, freq=50, gpioType=gpio.BCM): # freq in MHz
        gpio.setmode(gpioType)

        gpio.setup(SH_CP, gpio.OUT, initial=gpio.LOW)
        self.clock = SH_CP
        gpio.setup(DS, gpio.OUT, initial=gpio.LOW)
        self.data = DS
        gpio.setup(ST_CP, gpio.OUT, initial=gpio.LOW)
        self.latch = ST_CP

        self.nChain = nChain
        self.nOutput = nOutput
        self.period = (1/(freq*(10**6)))

    def writeOnShiftReg(self, data):
        if(len(data) != (self.nChain*self.nOutput)):
            return "Error : Bad Data length : {}, {} is required with {} registers".format(len(data), self.nChain*self.nOutput, self.nChain)
        else:
            for cell in range(len(data)):
                gpio.output(self.data, gpio.LOW if data[cell]==0 else gpio.HIGH)
                time.sleep(self.period/10)
                gpio.output(self.clock, gpio.HIGH)
                time.sleep(self.period)
                gpio.output(self.data, gpio.LOW)
                time.sleep(self.period/10)
                gpio.output(self.clock, gpio.LOW)
                time.sleep(self.period)

            gpio.output(self.latch, gpio.HIGH)
            time.sleep(self.period)
            gpio.output(self.latch, gpio.LOW)

if __name__ == "__main__":
    ist = DistriHandler(5, 12, 6, freq=0.125)
    while True:
        ist.writeOnShiftReg([1, 0, 1, 0, 0, 1, 1, 1])
        time.sleep(0.5)
