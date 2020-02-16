from machine import Pin, PWM, ADC

# ハードウェア設定
sw1 = Pin( 0, Pin.IN, Pin.PULL_UP)
sw2 = Pin( 4, Pin.IN, Pin.PULL_UP)
sw3 = Pin(16, Pin.IN, Pin.PULL_UP)
mtr = Pin(15, Pin.OUT, value=0)
brk = Pin( 2, Pin.OUT, value=0)

# 昇圧回路駆動 ブレーキ動作に必要
pulse = PWM(Pin(23), freq=75000, duty=512)

# ロータリエンコーダ出力値の取得
sens1 = ADC(Pin(36))
sens1.atten(ADC.ATTN_6DB)
sens1.width(ADC.WIDTH_10BIT)

import wifi
wifi.connectWifi()


import os

def ls():
    print(os.listdir("."))

def rm(fname):
    os.remove(fname)
