# simple speed control

from machine import ADC, Pin
from utime

target_speed = 1.0


enc = ADC(36)
sw  = Pin(0, Pin.IN, Pin.PULL_UP)
mtr = Pin(15, Pin.OUT, value=0)



adc_max, adc_min = -1,-1
def check_encoder_range():

    global adc_max, adc_min

    st = utime.ticks_ms()
    adcvals = []
    while utime.tics_diff(utime.ticks_ms(), st)<1000:
        adcvals.append(enc.read_u16())

    adc_max = max(adcvals)
    adc_min = min(adcvals)



encstat = "unknown"
_speed  = 0

def calc_speed(period):
    global _speed
    r = 25.6
    speed = r*3.14159/6/period

def enc_speed():
    if encstat == "unknown":
        adc_max, adc_min = check_encoder_range()
        adc_th_H = (adc_max*3+adc_min)/4
        adc_th_L = (adc_max+adc_min*3)/4

        while enc.read_u16()>adc_th_L:
            pass
        while enc.read_u16()<adc_th_H:
            pass
        st = utime.ticks_ms()
        while enc.read_u16()>adc_th_L:
            pass
        while enc.read_u16()<adc_th_H:
            pass
        period = utime.ticks_diff(utime.ticks_ms(), st)
        calc_speed(period)
        encstat = "high"

    encval = enc.read_u16()
    if encstat == "low" and encval > adc_th_H:
        cur = utime.ticks_ms()
        period = utime.ticks_diff(utime.ticks_ms(), st)
        calc_speed(period)
        st = cur
        encstat = "high"

    if encstat == "high" and encval < adc_th_L:
        encstat = "low"

    return _speed



def main():

    while sw1.value() == 0:
        pass
    while sw1.value() == 1:
        pass

    check_encoder_range()

    utime.sleep(2)

    sttime = utime.ticks_ms()
    while True:
        spd = enc_speed()
        if spd > target_speed:
            mtr.off()
            mtrstat = 0
        else:
            mtr.on()
            mtrstat = 1
        curtime = utime.ticks_diff(utime.ticks_ms(), sttime)
        with open("logfile", "a") as f:
            f.write("{},{},{}\n".format( curtime, spd, mtrstat ))

        if curtime>10000:
            break

    mtr.off()



main():
