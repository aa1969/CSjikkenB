from gpiozero import OutputDevice
import time
 # LED接続GPIO端⼦番号  
LED_PIN = 4
 # LED⽤の出⼒端⼦を⽣成する
led = OutputDevice(LED_PIN)
while True:
    # LED接続端⼦をHighにする
    led.on()
    time.sleep(1)
    # LED接続端⼦をLowにする
    led.off()
    time.sleep(1)