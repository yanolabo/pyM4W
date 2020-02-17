from machine import Pin, PWM, ADC, I2C

# ハードウェア設定
sw1 = Pin( 0, Pin.IN, Pin.PULL_UP)
sw2 = Pin( 4, Pin.IN, Pin.PULL_UP)
sw3 = Pin(16, Pin.IN, Pin.PULL_UP)

import motor
mtr = motor.Motor()

led1 = Pin(17, Pin.OUT, value=0)
led2 = Pin( 5, Pin.OUT, value=0)

# ロータリエンコーダ出力値の取得
sens1 = ADC(Pin(36))
sens1.atten(ADC.ATTN_6DB)
sens1.width(ADC.WIDTH_10BIT)


# MPU-6050
import mpu6050
i2c = I2C(scl=Pin(22), sda=Pin(21))
imu = mpu6050.imu(i2c)

import wifi
ip = wifi.connectWifi()

import utelnetd
utelnetd.start()

import uftpd
print("FTP server :: ftp://{}/".format(ip[0]) )

import os

def ls():
    print(os.listdir("."))

def rm(fname):
    os.remove(fname)
