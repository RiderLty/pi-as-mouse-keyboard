import json
import math
import os
import random
import socket
import threading
import time
from concurrent.futures import thread
from queue import Queue

import RPi.GPIO as GPIO

from utils.defines import *
from utils.interface import *


def atomWarpper(func):
    lock = threading.Lock()

    def f(*args, **kwargs):
        lock.acquire()
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return result

    return f


class ViewController:
    def __init__(self, path, x_range, y_range) -> None:
        self.mouse = Mouse(path)
        self.x_range = x_range
        self.y_range = y_range
        self.x = 0
        self.y = 0
        self.dowing = False
        self.no_move_count = 0
        self.running = True
        threading.Thread(target=self.autoRelese).start()

    def autoRelese(self):
        while self.running:
            if self.no_move_count <= 250:
                self.no_move_count += 1
                if self.no_move_count == 250:
                    self.reset()
            time.sleep(1 / 1000)

    @atomWarpper
    def left_with_lock(self, down):
        self.dowing = down
        self.mouse.report(l=down)

    def reset(self):
        self.x = 0
        self.y = 0
        self.dowing = False
        self.mouse.report(l=False)
        self.mouse.report(x=3000, y=3000)
        self.mouse.report(x=3000, y=3000)
        time.sleep(0.01)
        self.mouse.report(x=-2200, y=-1700)

    def moveView(self, x, y):
        self.no_move_count = 0
        self.x += x
        self.y += y
        if abs(self.x) > self.x_range or abs(self.y) > self.y_range:
            self.reset()
        self.x += x
        self.y += y
        if not self.dowing:
            self.dowing = True
            self.mouse.report(l=True)
        self.mouse.report(x=x, y=y)

    def stop(self):
        self.running = False
        self.mouse.__del__()


class recver:
    def __init__(self, port=9999, handeler=lambda data: print("raw : ", data)) -> None:
        self.handeler = handeler
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', port))

    def mainLoop(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            if data == b'stop':
                break
            self.handeler(data)

    def __del__(self):
        self.socket.close()


class gpioController:
    def __init__(self) -> None:
        GPIO.setmode(GPIO.BCM)          ## 使用BCM引脚编号，此外还有 GPIO.BOARD
        GPIO.setwarnings(False)
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.LOW) 

        GPIO.setup(18, GPIO.OUT)
        GPIO.output(18, GPIO.LOW) 

        self.wasd = {
            KEY_W: False,
            KEY_A: False,
            KEY_S: False,
            KEY_D: False,
        }
        self.wheelPingMap = ["wheel_pin_0","wheel_pin_1", "wheel_pin_2", "wheel_pin_3",
                             "wheel_pin_4", "wheel_pin_5", "wheel_pin_6", "wheel_pin_7", "wheel_pin_8"]
        self.wheelNow = self.wheelPingMap[4]
        self.key_map_wasd = [KEY_W, KEY_A, KEY_S, KEY_D]
        self.key_map_normal = {
            KEY_1: 17,
            KEY_2: 18,
        }
        self.wheelDown = False

        self.running = True
        self.eventqueue = Queue()
        threading.Thread(target=self.mainLoop).start()

    def stop(self):
        self.running = False
        self.putEvent(b'stop', False)

    def setBtn(self, pin, connect):
        print(f"set {pin} to {connect}")
        GPIO.output(pin, GPIO.HIGH if connect else GPIO.LOW)

    def onWASD(self, keycode: bytes, down: bool):
        self.wasd[keycode] = down
        mapVal = 4
        mapVal += -1 if self.wasd[KEY_A] else 0
        mapVal += 1 if self.wasd[KEY_D] else 0
        mapVal += -3 if self.wasd[KEY_S] else 0
        mapVal += 3 if self.wasd[KEY_W] else 0
        if mapVal == 4:#如果目标值为4 即中心
            self.setBtn(self.wheelNow, False)#释放当前按钮
            self.wheelNow = self.wheelPingMap[4]#设置当前为中心
            self.wheelDown = False#wheel状态为抬起
        else:
            if self.wheelDown == False:#如果从抬起到按下
                self.setBtn(self.wheelPingMap[4], True)
                time.sleep(1 / 1)
                self.setBtn(self.wheelPingMap[4], False)
                self.setBtn(self.wheelPingMap[mapVal],True)
                self.wheelNow = self.wheelPingMap[mapVal]
                self.wheelDown = True
            else:#从一个方向到另一个方向
                self.setBtn(self.wheelNow, False)
                # time.sleep(1 / 1)
                self.setBtn(self.wheelPingMap[mapVal], True)
                self.wheelNow = self.wheelPingMap[mapVal]


    def mainLoop(self):
        while self.running:
            keycode,down = self.eventqueue.get()
            if keycode == b'stop' and down == False:
                break
            else:
                self.handelKeyEvent(keycode, down)    


    def handelKeyEvent(self, keycode: bytes, down: bool):
        print("handelKeyEvent", keycode, down)
        
        if keycode in self.key_map_wasd:
            self.onWASD(keycode, down)
        elif keycode in self.key_map_normal:
            pin = self.key_map_normal[keycode]
            self.setBtn(pin, down)

    def putEvent(self, keycode: bytes, down: bool):
        self.eventqueue.put((keycode, down))



v = ViewController(r'/dev/hidg1', 2000, 2000)
gpioc = gpioController()


def handeler(bytes_data):
    data = json.loads(bytes_data.decode("utf-8"))
    if data["type"] == "mouse_move":
        x, y = data["data"]
        v.moveView(x, y)
        print(x, y)
    elif data["type"] == "key":
        keycode_int, down = data["data"]
        keycode = keycode_int.to_bytes(1, byteorder="big", signed=False)
        gpioc.putEvent(keycode, down)


recver(port=8848, handeler=handeler).mainLoop()
v.stop()
gpioc.stop()

# 插入ipad步骤
# 先插入HUB
# HUB连接电源
# 插入一个耗电设备 ，键盘 风扇啥的都行
# 插入树莓派
