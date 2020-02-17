from machine import PWM, Pin, ADC
import time

class Motor:
    st_brk = 0

    def __init__(self):
        #mtr = Pin(15, Pin.OUT, value=0)
        Motor.motor = PWM(Pin(15), freq=200, duty=0)
        Motor.brake = Pin( 2, Pin.OUT, value=0)

        # 昇圧回路駆動 ブレーキ動作に必要
        Motor.pulse = PWM(Pin(23), freq=75000, duty=512)

    def val(self, v):
        if v < 0:
            Motor.st_brk = 1
            Motor.motor.duty(0)
            time.sleep_ms(1)
            Motor.brake.on()
            return

        if v>100:
            v=100

        if Motor.st_brk == 1:
            Motor.st_brk = 0
            Motor.brake.off()
            time.sleep_ms(2)

        rate = int(1023*v/100)
        Motor.motor.duty( rate )

        return

# main test
if __name__ == "__main__":
    mtr = Motor()

    sw1 = Pin( 0, Pin.IN, Pin.PULL_UP)
    sw2 = Pin( 4, Pin.IN, Pin.PULL_UP)

    # ロータリエンコーダ出力値の取得
    sens1 = ADC(Pin(36))
    sens1.atten(ADC.ATTN_6DB)
    sens1.width(ADC.WIDTH_10BIT)

    while True:

        if sw1.value() == 0:
            mtr.val(100)
        else:
            mtr.val(0)

        if sw2.value() == 0:
            mtr.val(-1)

        # エンコーダの値を表示
        print(sens1.read())
