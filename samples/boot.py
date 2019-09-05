import machine
from machine import Pin, PWM, ADC
import time

# ハードウェア設定
sw1  = Pin( 0, Pin.IN, Pin.PULL_UP)
sw2  = Pin( 4, Pin.IN, Pin.PULL_UP)
sw3  = Pin(16, Pin.IN, Pin.PULL_UP)

mtr = Pin(15, Pin.OUT, value=0)
brk = Pin( 2, Pin.OUT, value=0)
# 昇圧回路駆動
pulse = PWM(Pin(23), freq=75000, duty=512)
