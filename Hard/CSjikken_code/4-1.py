import smbus
import time
import mcp3424
from gpiozero import InputDevice
from gpiozero import OutputDevice

i2c = smbus.SMBus(1)
addr = 0x68

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


i = 0 #モーター1
j = 0 #モーター2
k = 0 #時間管理用
isForward = False
isTurnRight=False
isTurnLeft=False
while True:
    k += 1
    if(k%200==0):
        config1 = (mcp3424.cfg_read | mcp3424.cfg_ch1 | mcp3424.cfg_once |
                mcp3424.cfg_12bit | mcp3424.cfg_PGAx1)
        config2 = (mcp3424.cfg_read | mcp3424.cfg_ch2 | mcp3424.cfg_once |
                mcp3424.cfg_12bit | mcp3424.cfg_PGAx1)
        config3 = (mcp3424.cfg_read | mcp3424.cfg_ch3 | mcp3424.cfg_once |
                mcp3424.cfg_12bit | mcp3424.cfg_PGAx1)
        
        # ch1
        data1 = i2c.write_byte(addr, config1)
        time.sleep(1 / mcp3424.sps_12bit)
        while True:
            data1 = i2c.read_i2c_block_data(addr, 0, 3)  # Read the current value
            if data1[2] >> 7 == 0:
                break
            time.sleep(0.001)
        volt1 = mcp3424.to_volt(data1, 12)    

        # ch2
        data2 = i2c.write_byte(addr, config2)
        time.sleep(1 / mcp3424.sps_12bit)
        while True:
            data2 = i2c.read_i2c_block_data(addr, 0, 3)  # Read the current value
            if data2[2] >> 7 == 0:
                break
            time.sleep(0.001)
        volt2 = mcp3424.to_volt(data2, 12)    

        # ch3
        data3 = i2c.write_byte(addr, config3)
        time.sleep(1 / mcp3424.sps_12bit)
        while True:
            data3 = i2c.read_i2c_block_data(addr, 0, 3)  # Read the current value
            if data3[2] >> 7 == 0:
                break
            time.sleep(0.001)        
        volt3 = mcp3424.to_volt(data3, 12)
        print("ch1:"+ str(volt1) + "ch2:"+ str(volt2) + "ch3:"+ str(volt3))

        if volt2 < 1.0:
            isForward = True
            isTurnRight=False
            isTurnLeft=False
        elif volt1 > volt3:
            isForward = False
            isTurnRight=True
            isTurnLeft=False
        else:
            isForward = False
            isTurnRight=False
            isTurnLeft=True    

        if volt1 > 1.7:
            isForward = False
            isTurnRight=True
            isTurnLeft=False
        if volt3 > 1.7:
            isForward = False
            isTurnRight=False
            isTurnLeft=True   

    #print(isForward)    
    if(isForward == True):
        i += 1
        if i >= 4:
            i = 0
        j -=1
        if j <= -1:
            j = 3    

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
     
