import time
import network

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)

    if wifi.isconnected():
        print('already Connected.')
        return wifi

    else:
        wifi.active(True)
        wifi.connect(ssid, passkey)
        while not wifi.isconnected() and timeout > 0:
            print('.')
            time.sleep(1)
            timeout -= 1

    if wifi.isconnected():
        print('Connected')
        return wifi

    else:
        print('Connection failed!')
        return null

wifi = connect_wifi("yanolab", "yanoyano")
if not wifi :
    sys.exit(0)
