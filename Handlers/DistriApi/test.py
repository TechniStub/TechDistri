import RPi.GPIO as gpio
import time
from handler import DistriHandler

ist = DistriHandler(5, 12, 6, freq=0.125)

while True:
    x=input("[y/n] : ")
    if x=="y":
        reg = [1, 1, 1, 1, 1, 1, 1, 1]
    else:
        reg = [0, 0, 0, 0, 0, 0, 0, 0]
    print(reg)
    ist.writeOnShiftReg(reg)
    time.sleep(1)
