# Mini4WD Development by ESP32 python

- setup/     セットアップファイル
- hardware/  ハードウェア情報
- samples/   ハードウェア制御プログラム


MicroPython ドキュメンテーション
--------------------------------
日本語資料
  https://micropython-docs-ja.readthedocs.io/ja/latest/index.html

ESP32用資料
  https://micropython-docs-ja.readthedocs.io/ja/latest/esp32/quickref.html


Setup
=====

esptool.py のインストール
--------------------------

`pip install esptool`
詳細：https://github.com/espressif/esptool

Windows の場合は下記から Flash Download Tools を入手
https://www.espressif.com/en/support/download/other-tools

シリアルケーブルの接続
----------------------

PCとマイコンをシリアルケーブルで接続する。
pl2303 搭載のシリアルケーブルを利用する。
Windows の場合はドライバが必要。Windows 8/10は本家でサポートを停止。
下記を参照してWindows にパッチを当てるとインストールできる。
http://www.ifamilysoftware.com/news37.html


シリアル通信用プログラムとして、
Linux や Mac では picocom や screen が利用できる。
Windows では TeraTerm や putty が利用できる。
通信速度は 115200bps である。

正しく接続した状態で、SW1を押しながら Reset すると
" Download Mode "に入ることが確認できる。
（補足）何も押さずに Reset すると内蔵ファームウェアの動作モード

Download モードにした状態でシリアル通信を終了する。
（補足）マイコンはダウンロードモードで待機している


ファームウェアの準備と書き込み
------------------------------

MAC
`esptool.py --chip esp32 --port /dev/tty.SLAB_USBtoUART write_flash -z 0x1000 esp32-20YYMMDD-vV.V.V.bin`

Linux
`esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20YYMMDD-vV.V.V.bin`

Windows
Flash Download Tools の GUI 画面にて
