base files for develop
======================

- boot.py
- wifi.py
- uftpd.py
- utelnetd.py


uftpd
-----

下記の improved のを入手。バックグラウンドで動作する。

https://github.com/cpopp/MicroFTPServer .. original uftpd
https://github.com/robert-hh/FTP-Server-for-ESP8266-ESP32-and-PYBD .. improved uftpd


utelnetd
--------

下記から utelnetserver.py を入手。新しい micropython では動作しないので
下記の差分の通りファイルを修正し、 utelnetd.py としてアップロードする。

https://github.com/cpopp/MicroTelnetServer .. original telnetd
```
$ diff -u utelnetserver.py.org utelnetserver.py
--- utelnetserver.py.org	2018-10-10 23:33:30.334417591 +0900
+++ utelnetserver.py	2018-10-10 23:34:58.326768231 +0900
@@ -2,12 +2,13 @@
 import network
 import uos
 import errno
+import io

 last_client_socket = None
 server_socket = None

 # Provide necessary functions for dupterm and replace telnet control characters that come in.
-class TelnetWrapper():
+class TelnetWrapper(io.IOBase):
     def __init__(self, socket):
         self.socket = socket
         self.discard_count = 0
```
