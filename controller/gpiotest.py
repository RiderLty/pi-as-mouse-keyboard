import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # 使用BCM引脚编号，此外还有 GPIO.BOARD
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
GPIO.setwarnings(False)


try:
    while True:
        GPIO.output(17, GPIO.HIGH)
        print("17 -> HIGH")
        time.sleep(0.01)
        GPIO.output(17, GPIO.LOW)
        print("17 -> LOW")
        time.sleep(0.5)
        GPIO.output(18, GPIO.HIGH)
        print("18 -> HIGH")
        time.sleep(0.01)
        GPIO.output(18, GPIO.LOW)
        print("18 -> LOW")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("exit")
    GPIO.output(17, GPIO.LOW)
    print("17 -> LOW")
    GPIO.output(18, GPIO.LOW)
    print("18 -> LOW")
