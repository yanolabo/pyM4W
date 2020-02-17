import time

def main():
    course = select_course()-1

    for x in range(3):
        course = run( course )


def wait_gz_more(val, stat="occer"):

    while True:
        imuval = imu.get_values()
        gz = imuval["GyZ"]
        print(gz,val, "more")
        if gz<val:
            continue
        if stat != "keep":
            # 検出時点で終了
            return
        break

    # 継続確認
    while True:
        imuval = imu.get_values()
        gz = imuval["GyZ"]
        print(gz,val, "more", "keep")
        if gz>val:
            continue
        break
    return

def wait_gz_less(val, stat="occer"):

    while True:
        imuval = imu.get_values()
        gz = imuval["GyZ"]
        print(gz,val, "less")
        if gz>val:
            continue
        if stat != "keep":
            # 検出時点で終了
            return
        break

    # 継続確認
    while True:
        imuval = imu.get_values()
        gz = imuval["GyZ"]
        print(gz,val, "less", "keep")
        if gz<val:
            continue
        break
    return


def run( c ):

    if c == 0:
        mtr.val(20)
        wait_gz_more(1000, "keep")
        time.sleep_ms(1020)
        wait_gz_more(1000, "keep")
        mtr.val(0)

        while True:
            pass
    elif c == 1:
        pass
    elif c == 2:
        pass

    next_c = 0
    time.sleep(1)
    return next_c



def getkey(wait):
    swcode = { (0,1,1):1, (1,0,1):2, (1,1,0):3 }
    ledstat = 1

    while True:
        led2.value(ledstat)
        ledstat = 1 - ledstat
        time.sleep_ms(wait)
        v = swcode.get( (sw1.value(), sw2.value(), sw3.value()), 0)
        if v != 0:
            break

    sel = v
    led2.off()
    time.sleep_ms(100)

    while True: # release detection
        v = swcode.get( (sw1.value(), sw2.value(), sw3.value()), 0 )
        if v == 0:
            break

    time.sleep(1)
    return sel


def select_course():

    while True:
        print("wait course selection")
        sel = getkey(250)
        print("Selected course : ", sel)

        time.sleep_ms(500)

        print("wait confirmation")
        if getkey(100) != 3:
            print("Confirmed..")
            break

        print("CANCEL")

    return sel




main()
