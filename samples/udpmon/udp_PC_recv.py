#!/usr/bin/python3

from socket import socket, AF_INET, SOCK_DGRAM

HOST = ''
PORT = 1169

# ソケットを開いて待受けする
s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    msg, addr = s.recvfrom(8192)           # データ受信
    print(f"{addr}:{msg}")

# socket 終了
s.close()
