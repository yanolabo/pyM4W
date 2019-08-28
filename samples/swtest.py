import machine
from machine import Pin

# Hardware Setup
sw1  = Pin( 0, Pin.IN, Pin.PULL_UP)
sw2  = Pin( 4, Pin.IN, Pin.PULL_UP)
sw3  = Pin(16, Pin.IN, Pin.PULL_UP)

while True:
    # pin の値参照は .value() で。
    print( sw1.value(), sw2.value(), sw3.value() )
