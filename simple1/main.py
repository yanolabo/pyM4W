import time

def main():
    course = select_course()-1

    for x in range(3):
        course = run( course )


def gz_more(val, stat):
    while True:
        imuval = imu.get_values()
        gz = imuval["GyZ"]

        print(gz)



def run( c ):

    if c == 0:
        wait_event("", "")
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
