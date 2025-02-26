# Othello (リバーシ) ゲーム

## 概要
このプロジェクトは、Python (Pygame) を使用してオセロ (リバーシ) を実装し、ESP32 との通信を行うシステムです。
ゲームロジックとその実装を備えており、プレイヤーの操作がESP32に送信されます。

## ファイル構成１（Pythonでの処理）
```
├── GameLogicPCC2.py  # ゲームのロジック
├── PCC1.py            # PygameによるGUIとESP32通信
└── __pycache__/       # Pythonのキャッシュフォルダ
```
## ファイル構成２(ESPでの処理)
```
ESP32Receiving
├── ESP32receiver.ino  # Pygameから信号を取得
├── LED_control.cpp    # PygameによるLEDの操作
└── LED_control.h      # ESP32Receiverからの信号をLED_controlへ繋ぐ
```
### `GameLogicPCC2.py`
- 盤面の初期化
- 有効な手の判定 (`is_valid_move`)
- 石を置く (`place_piece`)
- ゲーム終了判定 (`check_game_end`)

### `PCC1.py`
- Pygameを使ったボードの描画 (`draw_board`)
- マウスクリックによるプレイヤーの操作
- ESP32への手の送信 (`send_move_to_esp32`)

## 環境設定
### 必要なライブラリ
以下のライブラリをインストールしてください。
```sh
pip install pygame pyserial
FastLED.h
```

### ESP32との接続
ESP32とBluetoothで通信するため、適切なCOMポートを設定してください。
デフォルトは `COM12` です。

```python
ESP32_COM_PORT = "COM13"  # 必要に応じて変更
BAUD_RATE = 115200
```

## 遊び方
1. `PCC1.py` を実行すると、オセロの画面が表示されます。
2. マウスでボード上をクリックして石を置きます。
3. 各ターンの手がESP32に送信されます。
4. 両プレイヤーが有効な手を打てなくなると、ゲーム終了。

## 注意事項
- Pygameのウィンドウを閉じるとゲームが終了します。
- LEDところに少し誤作動があるため、デバッグが必要です。

