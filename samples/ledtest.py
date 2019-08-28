import machine
from machine import Pin, PWM
import time

# ハードウェア設定
led2 = Pin( 5, Pin.OUT)

# PWM 設定
led1pwm = PWM(Pin(17, Pin.OUT))
led1pwm.freq(100000)
duty = 0

while True:

    if duty >= 1024:
        duty = 0
    else:
        duty += 100

    # 点滅処理
    led2.value( 1 - led2.value() )

    # 輝度の変更
    led1pwm.duty(duty)

    print( led2.value(), duty )


    # 一時停止
    time.sleep(0.1)


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
