import socket

HOSTIP = "192.168.8.175"
PORT = 1169

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("> ")
    sock.sendto(msg, (HOSTIP, PORT))

s.close()
