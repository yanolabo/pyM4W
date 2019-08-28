import machine
from machine import Pin

# ハードウェア設定
led1 = Pin(17, Pin.OUT)
led2 = Pin( 5, Pin.OUT)

sw1  = Pin( 0, Pin.IN, Pin.PULL_UP)
sw2  = Pin( 4, Pin.IN, Pin.PULL_UP)
sw3  = Pin(16, Pin.IN, Pin.PULL_UP)


while True:

    # sw1 の状態を LED 1 に表示
    led1.value( 1 - sw1.value() )

    # SW2, SW3 で ON/OFF の切り替え
    if not sw2.value():     # push sw2
        led2.value(1)
    if sw3.value() == 0:  # push sw3
        led2.off()

"""
Pin. class
__class__       value           IN              IRQ_FALLING
IRQ_RISING      OPEN_DRAIN      OUT             PULL_DOWN
PULL_HOLD       PULL_UP         WAKE_HIGH       WAKE_LOW
init            irq             off             on
"""
