from gpiozero import OutputDevice
import time

# ステッピングモータ接続GPIO端⼦番号
OUTPUT_PIN1_1 = 6
OUTPUT_PIN1_2 = 13
OUTPUT_PIN1_3 = 19
OUTPUT_PIN1_4 = 26

# モータを回転させる際の間隔
TIME_SLEEP = 0.002

# モータ⽤の出⼒端⼦を⽣成する
motor_pins = [
    OutputDevice(OUTPUT_PIN1_1),
    OutputDevice(OUTPUT_PIN1_2),
    OutputDevice(OUTPUT_PIN1_3),
    OutputDevice(OUTPUT_PIN1_4),
]

# 指定した1相のみを励磁する関数
def out_motor_pin(pin_num):
    for i in range(0, 4):
        if i == pin_num:
            motor_pins[i].on()
        else:
            motor_pins[i].off()



# 1相励磁によるステッピングモータ運転
while True:
    i = 0
    for j in range(0, 1000):   
        out_motor_pin(i)
        i += 1
        if i >= 4:
            i = 0 # ⼀周したら戻る
        # 乱調を避けるために少し待つ
        time.sleep(TIME_SLEEP)

    i = 3
    for j in range(0, 1000):   
        out_motor_pin(i)
        i -= 1
        if i <= -1:
            i = 3 # ⼀周したら戻る
        # 乱調を避けるために少し待つ
        time.sleep(TIME_SLEEP)

    for j in range(0, 1000):   
        out_motor_pin(i)

        # 乱調を避けるために少し待つ
        time.sleep(TIME_SLEEP)         