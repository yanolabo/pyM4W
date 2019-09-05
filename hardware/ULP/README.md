ULP( Ultra Low Power ) の活用
=============================

概要
----

単体コンパイラ
 https://github.com/espressif/binutils-esp32ulp/releases


ドキュメント
 https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/ulp.html

ULP をコントロールする API が micropython の esp32 モジュール から呼び出しできる
 https://micropython-docs-ja.readthedocs.io/ja/latest/esp32/quickref.html#installing-micropython


```
import esp32
ulp = esp32.ULP()

ulp.load_binary()
ulp.run()
ulp.set_wakeup_period()
```

CPU と ULP の通信は RTC slow memory を利用する。

CPU 側からは次のように使う。
```
value = machine.mem32[0x50000000 + offset] # read  RTC_SLOW_MEM
machine.mem32[0x50000000 + offset] = value # write RTC_SLOW_MEM
# 32bit 単位なので offset は 4 の倍数

value = machine.mem8[0x50000000 + offset] # read  RTC_SLOW_MEM
machine.mem8[0x50000000 + offset] = value # write RTC_SLOW_MEM
# 8bit 単位なので offset は 自然数

```



good example with esp32_lp
-----------------------------

https://github.com/ThomasWaldmann/py-esp32-ulp/blob/master/examples/counter.py
```
"""
Very basic example showing data exchange main CPU <--> ULP coprocessor.
To show that the ULP is doing something, it just increments the value <data>.
It does that once per ulp timer wakeup (and then the ULP halts until it gets
waked up via the timer again).
The timer is set to a rather long period, so you can watch the data value
incrementing (see loop at the end).
"""

from esp32 import ULP
from machine import mem32

from esp32_ulp.__main__ import src_to_binary

source = """\
data:       .long 0
entry:      move r3, data    # load address of data into r3
            ld r2, r3, 0     # load data contents ([r3+0]) into r2
            add r2, r2, 1    # increment r2
            st r2, r3, 0     # store r2 contents into data ([r3+0])
            halt             # halt ULP co-prozessor (until it gets waked up again)
"""

binary = src_to_binary(source)

load_addr, entry_addr = 0, 4

ULP_MEM_BASE = 0x50000000
ULP_DATA_MASK = 0xffff  # ULP data is only in lower 16 bits

ulp = ULP()
ulp.set_wakeup_period(0, 50000)  # use timer0, wakeup after 50.000 cycles
ulp.load_binary(load_addr, binary)

mem32[ULP_MEM_BASE + load_addr] = 0x1000
ulp.run(entry_addr)

while True:
    print(hex(mem32[ULP_MEM_BASE + load_addr] & ULP_DATA_MASK))
```
