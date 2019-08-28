import machine
from machine import Pin, PWM, ADC
import time

# ハードウェア設定
sw1 = Pin(0, Pin.IN, Pin.PULL_UP)
mtr = Pin(15, Pin.OUT, value=0)
brk = Pin( 2, Pin.OUT, value=0)

# 昇圧回路駆動
pulse = PWM(Pin(23), freq=75000, duty=512)

sens1 = ADC(Pin(36))
sens1.atten(ADC.ATTN_6DB)
sens1.width(ADC.WIDTH_10BIT)

while True:

    if sw1.value() == 1:
        mtr.off()
    else:
        mtr.on()

    print(sens1.read())


"""

Pin. class
__class__
value           IN              IRQ_FALLING     IRQ_RISING      OPEN_DRAIN
OUT             PULL_DOWN       PULL_HOLD       PULL_UP         WAKE_HIGH
WAKE_LOW        init            irq             off             on


PWM. class
__class__
deinit          duty            freq            init


"""
