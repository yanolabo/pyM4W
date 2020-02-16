# -*- coding:utf-8 -*-

import network
import time
import os

def connectWifi():
    global st

    # ファイルから接続先リストを取得
    ssid={}

    try:
        os.stat("wifi.conf")
    except OSError:
        print("No wifi.conf file. Wifi Setup aborted.")
        return None

    with open("wifi.conf", "r") as cfile:
        for each in cfile:
            if each[0]=="#":
                continue
            if "::" not in each:
                continue
            k,v = each.strip().split("::",1)
            ssid[k]=v

    # Wifi を起動
    st = network.WLAN(network.STA_IF)
    if st.isconnected() == True:
        print("Already Connected to WiFi AP")
        return st.ifconfig()
    st.active(True)

    # 基地局リストを取得
    ssidlist = [x[0].decode() for x in st.scan()]
    print(ssidlist)
    ssidlist.append("!")

    # 電波の強い順に接続先にあるかを確認
    for each in ssidlist:
        if each in ssid.keys():
            st.connect(each, ssid[each])
            break
    else:
        print("No known SSID, connection aborted.")
        return None

    # Wifi に接続する
    print("Connecting to", each, "....")
    while st.isconnected() == False:
        time.sleep(0.5)
        print(":")

    print("Wifi Connected!")
    ifconf = st.ifconfig()
    print(ifconf)

    return ifconf # 接続情報を返す


def disconnectWifi():
    global st

    st.active(False)



def startAP():
    try:
        os.stat("wifi.conf")
    except OSError:
        print("No wifi.conf file. Wifi Setup aborted.")
        return None

    with open("wifi.conf","r") as cfile:
        for each in cfile:
            if each[0]=="#":
                continue
            if ";;" not in each:
                continue
            ssid,pw = [x.encode() for x in each.strip().split(";;",1)]
            break
        else:
            print("No AP setting. AP Setup aborted.")
            return None

    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)

    if ssid.endswith("++"):
        import ubinascii
        ssid = ssid[:-2]+ubinascii.hexlify(ap.config("mac")[-3:])

    ap.config(essid=ssid, password=pw,
              authmode=network.AUTH_WPA_WPA2_PSK)
    print("AP started. SSID=[{}], pw=[{}]".format(ssid,pw))
    return ap

def stopAP():
    global ap

    ap.config(essid="noap", password="00000000",
              authmode=network.AUTH_WPA_WPA2_PSK)
    ap.active(False)

# "ssidlist"ファイルにある WiFi基地局に接続します。
# ip = connectWifi()

