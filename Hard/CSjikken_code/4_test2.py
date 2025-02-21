import smbus
import time
import mcp3424
from gpiozero import InputDevice
from gpiozero import OutputDevice


#センサ左 ch1
#センサ前 ch2
#センサ右 ch3

# ステッピングモータ接続GPIO端⼦番号
OUTPUT_PIN1_1 = 6
OUTPUT_PIN1_2 = 13
OUTPUT_PIN1_3 = 19
OUTPUT_PIN1_4 = 26

OUTPUT_PIN2_1 = 4
OUTPUT_PIN2_2 = 17
OUTPUT_PIN2_3 = 27
OUTPUT_PIN2_4 = 22

# モータを回転させる際の間隔
TIME_SLEEP = 0.002

# モータ⽤の出⼒端⼦を⽣成する
motor1_pins = [
    OutputDevice(OUTPUT_PIN1_1),
    OutputDevice(OUTPUT_PIN1_2),
    OutputDevice(OUTPUT_PIN1_3),
    OutputDevice(OUTPUT_PIN1_4),
]

motor2_pins = [
    OutputDevice(OUTPUT_PIN2_1),
    OutputDevice(OUTPUT_PIN2_2),
    OutputDevice(OUTPUT_PIN2_3),
    OutputDevice(OUTPUT_PIN2_4),
]

# モーター1の指定した1相のみを励磁する関数
def out_motor1_pin(pin_num):
    for i in range(0, 4):
        if i == pin_num:
            motor1_pins[i].on()
        else:
            motor1_pins[i].off()

# モーター2の指定した1相のみを励磁する関数
def out_motor2_pin(pin_num):
    for i in range(0, 4):
        if i == pin_num:
            motor2_pins[i].on()
        else:
            motor2_pins[i].off()   

# 1相励磁によるステッピングモータ運転
i = 0 #モーター1
j = 0 #モーター2
k = 0 #時間管理用
isForward = True
isTurnRight=False
isTurnLeft=False
while True: 
    if(isForward == True):
        i += 1
        if i >= 4:
            i = 0
        j -=1
        if j <= -1:
            j = 3
        print(i)        

    if(isTurnRight):
        i -= 1
        if i <= -1:
            i = 3
        j -=1
        if j <= -1:
            j = 3  

    if(isTurnLeft):
        i += 1
        if i >= 4:
            i = 0
        j +=1
        if j >= 4:
            j = 0
                      
    out_motor1_pin(i)
    out_motor2_pin(j)
    # 乱調を避けるために少し待つ
    time.sleep(TIME_SLEEP)    