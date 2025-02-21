from gpiozero import InputDevice
from gpiozero import OutputDevice
import time

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

# スイッチ接続GPIO端⼦番号
SW1_PIN = 5
SW2_PIN = 23
SW3_PIN = 16
SW4_PIN = 20
SW5_PIN = 21

# スイッチ⽤にプルアップモードで⼊⼒端⼦を⽣成する
switch1 = InputDevice(SW1_PIN, pull_up=True)
switch2 = InputDevice(SW2_PIN, pull_up=True)
switch3 = InputDevice(SW3_PIN, pull_up=True)
switch4 = InputDevice(SW4_PIN, pull_up=True)
switch5 = InputDevice(SW5_PIN, pull_up=True)

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

isForward=False
isBack=False
isStopped=False
isTurnRight=False
isTurnLeft=False

i = 0 #モーター1
j = 0 #モーター2
while True:
    # スイッチ1接続端⼦の状態読み取り
    if switch1.value == 1:
        isForward = True #前進判定有効
        isBack=False
        isTurnRight=False
        isTurnLeft=False       
        print("Switch1 on")
        time.sleep(1)

    # スイッチ2接続端⼦の状態読み取り    
    if switch2.value == 1:
        isForward = False #前進判定無効
        isBack=True
        isTurnRight=False
        isTurnLeft=False     
        print("Switch2 on")
        time.sleep(1)

    # スイッチ3接続端⼦の状態読み取り
    if switch3.value == 1: 
        isForward = False
        isBack=False 
        isTurnLeft=False
        isTurnRight=True           
        print("Switch3 on")
        time.sleep(1)

    # スイッチ4接続端⼦の状態読み取り    
    if switch4.value == 1: 
        isForward = False
        isBack=False 
        isTurnLeft=True
        isTurnRight=False    
        print("Switch4 on")
        time.sleep(1)   

    # スイッチ5接続端⼦の状態読み取り    
    if switch5.value == 1: 
        if(isStopped == False):
            isStopped = True
        else:
            isStopped = False  
        print("Switch5 on")
        time.sleep(1)       

    if isStopped == True:
        time.sleep(1)
    else:
        if(isForward == True):
            i += 1
            if i >= 4:
                i = 0
            j -=1
            if j <= -1:
                j = 3

        if(isBack == True):
            i -= 1
            if i <= -1:
                i = 3
            j +=1
            if j >= 4:
                j = 0

        if(isTurnLeft):
            i += 1
            if i >= 4:
                i = 0
            j +=1
            if j >= 4:
                j = 0

        if(isTurnRight):
            i -= 1
            if i <= -1:
                i = 3
            j -=1
            if j <= -1:
                j = 3      
                      
        out_motor1_pin(i)
        out_motor2_pin(j)
        # 乱調を避けるために少し待つ
        time.sleep(TIME_SLEEP)                   
     

    
