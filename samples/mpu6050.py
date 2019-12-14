import machine


class imu():
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr

        # 0x6B : DevReset, Sleep, Cycle, -, TEMP_DS, CLKSEL[3..0]
        #           0        0      0    0    0       0:intOSC_8MHz
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([0x6B, 0x00]))
        self.i2c.stop()

        # gyro setup
        # 0x1B : XG_ST, YG_ST, ZG_ST, FS_SEL[1:0], -[3:0]
        #         1:start SelfTest     0:±250度/s, 1:500/s, 2:1000/s, 3:2000/s  000
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([0x1B, 0x08]))
        self.i2c.stop()
        # scale factor :: 0:131, 1:65.5, 2:32.8, 3:16.4 ( use for calcurate deg/s )

        # accel setup
        # 0x1C : XA_ST, YA_ST, ZA_ST, AFS_SEL[1:0], -[3:0]
        #         1:start SelfTest     0:±2g, 1:4g, 2:8g, 3:16g  000
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([0x1C, 0x10]))
        self.i2c.stop()
        # scale factor :: 0:16364, 1:8192, 2:4096, 3:2048 ( use for calcurate g )

        # LPF setup
        # 0x1A : -[1:0], EXT_SYNC_SET[2:0], DLPF_CFG[2:0]
        #          00      000               below
        #     A: Bandwidth(Hz) Delay(ms)  G: Bandwidth(Hz) Delay(ms)
        # 0     250              0          256              0
        # 1     164              2.0        188              1.9
        # 2      94              3.0         98              2.8
        # 3      44              4.9         42              4.8
        # 4      21              8.5         20              8.3
        # 5      10              13.8        10              13.4
        # 6       5              19.0         5              18.6
        self.i2c.start()
        self.i2c.writeto(self.addr, bytearray([0x1A, 0x03]))
        self.i2c.stop()



    def get_raw_values(self):
        self.i2c.start()
        a = self.i2c.readfrom_mem(self.addr, 0x3B, 14)
        self.i2c.stop()
        return a

    def get_ints(self):
        b = self.get_raw_values()
        c = []
        for i in b:
            c.append(i)
        return c

    def byte2int(self, firstbyte, secondbyte):
        if not firstbyte & 0x80:
            return firstbyte << 8 | secondbyte
        return - (((firstbyte ^ 255) << 8) | (secondbyte ^ 255) + 1)

    def get_values(self):
        raw_ints = self.get_raw_values()
        vals = {}
        vals["AcX"] = self.byte2int(raw_ints[0], raw_ints[1])
        vals["AcY"] = self.byte2int(raw_ints[2], raw_ints[3])
        vals["AcZ"] = self.byte2int(raw_ints[4], raw_ints[5])
        vals["Tmp"] = self.byte2int(raw_ints[6], raw_ints[7]) / 340.00 + 36.53
        vals["GyX"] = self.byte2int(raw_ints[8], raw_ints[9])
        vals["GyY"] = self.byte2int(raw_ints[10], raw_ints[11])
        vals["GyZ"] = self.byte2int(raw_ints[12], raw_ints[13])

        return vals  # returned in range of Int16
        # -32768 to 32767

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes I2C
        from time import sleep
        while True:
            print(self.get_values())
            sleep(0.05)


if __name__ == "__main__":
    i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
    imu_sensor = imu(i2c)

    while True:
        v = imu_sensor.get_values().values()
        print("{:7d} {:7d} {:7d} {:4.1f} {:7d} {:7d} {:7d}".format(*v))
