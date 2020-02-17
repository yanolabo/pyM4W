import socket

class udpsend():
    def __init__(self):

        try:
            with open("udpip.conf") as f:
                self.ip=f.read().strip()
        except:
            ip = input("UDP recv IP : ")
            with open("udpip.conf", "w") as f:
                f.write(ip)

        self.port = 1169

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def msg(self, txt):
        while True:
            try:
                self.sock.sendto(txt.encode(), (self.ip, self.port))
                break
            except:
                continue
        print(txt)
