import time
import machine
from machine import Pin, ADC

# ハードウェア設定
vLiPo = ADC(Pin(34))
vLiPo.atten(ADC.ATTN_11DB)  # 3.3V -> 4096
vLiPo.width(ADC.WIDTH_10BIT)

vAAA2 = ADC(Pin(35))
vAAA2.atten(ADC.ATTN_6DB)
vAAA2.width(ADC.WIDTH_10BIT)
# 2.0V -> 1024 ; 3.21V で 285
#                1.33V で  90


while True:

    print( vLiPo.read(), vAAA2.read() )

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

ADC. class
__class__
read            ATTN_0DB        ATTN_11DB       ATTN_2_5DB      ATTN_6DB
WIDTH_10BIT     WIDTH_11BIT     WIDTH_12BIT     WIDTH_9BIT      atten
width

ADC.ATTN_0DB   — the full range voltage: 1.2V
ADC.ATTN_2_5DB — the full range voltage: 1.5V
ADC.ATTN_6DB   — the full range voltage: 2.0V
ADC.ATTN_11DB  — the full range voltage: 3.3V

"""
