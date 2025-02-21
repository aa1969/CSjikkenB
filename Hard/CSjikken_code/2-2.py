from gpiozero import InputDevice
import time

# スイッチ接続GPIO端⼦番号
SW_PIN = 17

# スイッチ⽤にプルアップモードで⼊⼒端⼦を⽣成する
switch = InputDevice(SW_PIN, pull_up=True)

while True:
     # スイッチ接続端⼦の状態読み取り
    if switch.value == 1: # 押されていれば1（True）
        print("Switch on")
    else:
        print("Switch off")
    time.sleep(0.5)
