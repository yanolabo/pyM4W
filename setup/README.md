esp32 に micropython をインストールする
=======================================

準備
----

1. 必要なツールをインストールする。

```
sudo apt -y install picocom esptool python-pip
```


2. ファームウェアを入手する。

[本家](https://micropython.org/download#esp32)にある esp32-YYYYMMDD-vX.X.X-XXX-xxxxxxxxxx.bin をダウンロードする。
このファイルは毎日更新される。バージョン番号によって更新日が確認できる。
基本的には最新版を入手すると良い。

（参考までに、このフォルダ内に 2019/06/27 時点の最新安定版を入れておく）

これとは別に esp32spiram というバイナリもある。
こちらは pSRAM を搭載したモジュール用で、一般的な esp32 board には必要ない機能。

なお、micropython は python3 をベースとしているので、python2系に慣れている場合は注意。


3. ファイル転送ツールをインストールする

```
pip install adafruit-ampy
```

名称類似のパッケージに ampy があるが、別物なので注意。
ampy は Adafruit Micro PYthon の略。


書き込みと動作確認
------------------

```
esptool --chip esp32 --port /dev/ttyUSB0 -b 460800 write_flash -z 0x1000 esp32-YYYYMMDD-vX.X.X-XXX-xxxxxxxxxx.bin
```

書き込みの際には ESP32 を download mode にしておく。書き込みにはおよそ1分程度かかる。
本家には erase_flash を初回に行うよう指示があるが、lolin32 や TTGO で実行するとサポートしていないというメッセージが表示される。


ファームウェアを書き込んだらシリアルモニタの picocom を起動する。

```
picocom -b115200 /dev/ttyUSB0
```

picocom は キーボード入力をマイコンに転送するため、
picocom 自体の終了はショートカットキー( C-a C-q )を利用する。

モニターが起動しても何も表示変化はない。ここで esp32 board をリセットする。
すると、micropython の起動ログが確認できる。
確認したら、シリアルモニタを終了させる( C-a C-q )。

ファイルシステム上のファイルを確認する。

```
ampy -p /dev/ttyUSB0 ls -l
```

ファイルの一覧が得られ、boot.py が確認できる。
このファイルを取得しよう。

```
ampy -p /dev/ttyUSB0 get boot.py
```

get コマンドでファイルを取得し標準出力に表示できる。
ファイルを保存する場合はリダイレクトを使う。

```
ampy -p /dev/ttyUSB0 get boot.py > boot.py
```

いちいち PORT 指定がめんどうなら環境変数を設定すると良い。

```
export AMPY_PORT=/dev/ttyUSB0
```

ampy がサポートするコマンドには以下がある。

- put : ファイルをボードに転送する
- get : ボードのファイルを標準出力へ
- ls  : 一覧の表示。 -l オプションでファイルサイズも得られる。
- rm  : ファイルを削除。ファイルは1つづつ指定する。
- run : 指定したスクリプトを実行する。出力結果はそのまま標準出力にて確認できる

run 命令が非常に便利。

例えば、エディタで test.py を編集し、実行する場合は下記のようにすれば良い。
本フォルダ内の test.py を実行することでファイルの一覧を得ることができる。

```
ampy run test.py
```

下記のような Makefile を用意しておけば、make のみで最新のpyファイルを実行できるようになる。

```
ALL:
    ampy -p /dev/ttyUSB* run `ls -t *.py|head -1`
```

補足）emacs で開発する場合、`C-c c` で make が実行される。
