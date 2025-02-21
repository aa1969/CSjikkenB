from gpiozero import OutputDevice
import time

# ステッピングモータ接続GPIO端⼦番号
OUTPUT_PIN1_1 = 6
OUTPUT_PIN1_2 = 13
OUTPUT_PIN1_3 = 19
OUTPUT_PIN1_4 = 26

# 初期のモータ回転間隔
TIME_SLEEP_INITIAL = 0.01

# 定速運転時のモータ回転間隔
TIME_SLEEP_FASTEST = 0.002

# 加速・減速に使うステップ数
ACCELERATION_STEPS = 100

# 全体の運転ステップ数
TOTAL_STEPS = 1000

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


#台形加速開始

#最初のtime.sleepの時間
current_sleep = TIME_SLEEP_INITIAL

i = 0
# 加速区間
for step in range(ACCELERATION_STEPS):
    out_motor_pin(i)
    i = (i + 1) % 4
    time.sleep(current_sleep)
    
    # 加速：ステップごとに待機時間を短くしていく
    current_sleep -= (TIME_SLEEP_INITIAL - TIME_SLEEP_FASTEST) / ACCELERATION_STEPS
    if current_sleep < TIME_SLEEP_FASTEST:
        current_sleep = TIME_SLEEP_FASTEST

# 定速区間
for step in range(TOTAL_STEPS - 2 * ACCELERATION_STEPS):
    out_motor_pin(i)
    i = (i + 1) % 4
    time.sleep(current_sleep)

# 減速区間
for step in range(ACCELERATION_STEPS):
    out_motor_pin(i)
    i = (i + 1) % 4
    time.sleep(current_sleep)
    
    # 減速：ステップごとに待機時間を長くしていく
    current_sleep += (TIME_SLEEP_INITIAL - TIME_SLEEP_FASTEST) / ACCELERATION_STEPS
    if current_sleep > TIME_SLEEP_INITIAL:
        current_sleep = TIME_SLEEP_INITIAL



