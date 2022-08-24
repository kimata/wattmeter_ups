# UPS ワットメータ

## 概要

UPS の機能を使って消費電力を計測し，Fluentd に送信するスクリプトです．

## 準備

`config.yml` と `ups.yml` を書き換えて，Fluetd サーバやデバイス名の
変換に関する設定を行います．

`ups.yml` には，Network UPS Tools で接続した UPS を指定します．

## 使い方

```
python3 app/ups_nut_logger.py
```
