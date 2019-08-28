""" ピエゾブザー、スピーカー 駆動プログラム """

from machine import Pin, PWM
import time

# ハードウェア設定
ptz = PWM(Pin(25), freq=1, duty=0)

ptz.duty(512)   # 音を発生

ptz.freq(1000)
time.sleep(0.2)
ptz.freq(1500)
time.sleep(0.2)
ptz.freq(1800)
time.sleep(0.2)

ptz.duty(0)     # 音を止める



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
