from machine import Pin
import time

mtr = Pin(15, Pin.OUT, value=0)

i=0
while(i<5):
    mtr.on()
    time.sleep(3)
    mtr.off()
    time.sleep(3)

    i+=1
time.sleep(1)
