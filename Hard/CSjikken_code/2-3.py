from gpiozero import InputDevice
from gpiozero import OutputDevice
import time

 # LED接続GPIO端⼦番号  
LED1_PIN = 4
LED2_PIN = 17
LED3_PIN = 27
LED4_PIN = 22

 # LED⽤の出⼒端⼦を⽣成する
led1 = OutputDevice(LED1_PIN)   
led2 = OutputDevice(LED2_PIN)
led3 = OutputDevice(LED3_PIN)
led4 = OutputDevice(LED4_PIN)

# スイッチ接続GPIO端⼦番号
SW1_PIN = 5
SW2_PIN = 6

# スイッチ⽤にプルアップモードで⼊⼒端⼦を⽣成する
switch1 = InputDevice(SW1_PIN, pull_up=True)
switch2 = InputDevice(SW2_PIN, pull_up=True)

leds = [led1, led2, led3, led4]

isStopped=False
isReversed=False
i = 0

while True:
    
    # スイッチ1接続端⼦の状態読み取り
    if switch1.value == 1:
        if(isStopped == False):
            isStopped = True #止める判定
        else:
            isStopped = False #止める判定        
        print("Switch1 on")
    # スイッチ2接続端⼦の状態読み取り    
    if switch2.value == 1: 
        if(isReversed == False):
            isReversed = True #逆判定
        else:
            isReversed = False #逆判定
        print("Switch2 on")
    print(i)     
    if isStopped == True:
        time.sleep(1)
    else:
        if isReversed == True: 
            i-=1
        else:
            i+=1
        j = i%4   
        leds[j].on()                    
        time.sleep(0.5) 
        leds[j].off()                    
        time.sleep(0.5)      
    
