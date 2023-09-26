# -*- coding: utf-8 -*-
# Time : 2019/2/7 12:40
# Author : hubozhi
import json
import socket
import threading
import time
from concurrent.futures import thread
from math import *
from queue import Queue
from sys import exit

import pygame
from pygame.locals import *
from pygame.math import *

from utils.defines import *


class sender:
    def __init__(self, ip, port) -> None:
        self.target = (ip, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, data):
        self.socket.sendto(data, self.target)

    def __del__(self):
        self.socket.sendto(b'stop', self.target)
        self.socket.close()


lasttime = 0
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((320, 240), 0, 32)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    toPi = sender("192.168.1.180", 8848)



    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # simulategpio.stop()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # simulategpio.stop()
                    exit()
                data = json.dumps({
                    "type": "key",
                    "data": [event.scancode, True]
                })
                # print(data)
                toPi.send(data.encode("utf-8"))

            elif event.type == KEYUP:
                # print(event.scancode)
                data = json.dumps({
                    "type": "key",
                    "data": [event.scancode, False]
                })
                # print(data)
                toPi.send(data.encode("utf-8"))


            elif event.type == pygame.MOUSEBUTTONDOWN:
                print(f"{event.button} down")
            elif event.type == pygame.MOUSEBUTTONUP:
                print(f"{event.button} up")
            elif event.type == pygame.MOUSEMOTION:
                rel = pygame.mouse.get_rel()
                rate = time.time() - lasttime
                lasttime = time.time()
                mouserel = f"x:{rel[0]}, y:{rel[1]}   rate:{int(1/ (rate if rate != 0 else 1)   )}"
                data = json.dumps({
                    "type": "mouse_move",
                    "data": rel
                })

                toPi.send(data.encode("utf-8"))
                # print()
            elif event.type == pygame.MOUSEWHEEL:
                print(event.y)
