「XGP <-> ブラウザ」のためのツールセット
===

## 概要

[XGP](https://link.springer.com/article/10.1007/s10015-010-0857-9)から送られてくる[OSI参照モデル](https://qiita.com/tatsuya4150/items/474b60beed0c04d5d999)で言うところのL4なUDP StringをL7なHTTP JSONに変換し、その逆もしかりなツールセットです。

## シーケンス図

![Sequence image](20180104_sequence.png)

```sequence
XGP->UDP String Receiver: Send UDP String
UDP String Receiver->Active MQ: Queueing
Web Browser->HTTP Server for Sending JSON: Get JSON
HTTP Server for Sending JSON->Active MQ: Get queue
Web Browser->HTTP Server for Sending UDP String: Post JSON
HTTP Server for Sending UDP String->XGP: Send UDP String
```

## 使い方

黒い画面（ターミナル）でやる

### Python 3.x が入っているか確認

```
$ python3 --version
Python 3.6.3 <- これが出たらOK（3.x.yのxとyは適当）
```

#### bash: python3: command not found と表示された場合

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
$ brew install python3
$ python3 --version
```

### このリポジトリをcloneする

```
$ cd どこか適当なディレクトリ
$ git clone https://github.com/kimyan/xgp-transcoder.git
$ cd xgp-transcoder
```

### virtualenvの設定

```
$ python3 -m venv env
$ source env/bin/activate <- (env)と表示されていればOK。以後、これをやってから作業する。
```

### 必要なライブラリのインストール

```
(env)$ pip install -r requirements.txt
```

### 実行

#### ひとつめ

上の続きで

```
(env)$ python http-server-for-sending-json.py
```

#### ふたつめ

別窓を開く

```
$ cd xgp-transcoder <- 実際の置き場所に移動する
$ source env/bin/activate
(env)$ python http-server-for-sending-udp-string.py
```

#### みっつめ

別窓を開く

```
$ cd xgp-transcoder <- 実際の置き場所に移動する
$ source env/bin/activate
(env)$ python udp-string-receiver-for-sending-queue.py
```



