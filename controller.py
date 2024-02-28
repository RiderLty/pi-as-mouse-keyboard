import os
import socket
import struct

import pygame
from pygame.locals import *
from pygame.math import *

from utils.defines import *
from utils.interface import *

# kb = KeyBoard(r'/dev/hidg0')
# mouse = Mouse(r'/dev/hidg1')

kb = KeyBoard("192.168.3.104", 5643)
mouse = Mouse("192.168.3.104", 5644)


DOWN = 0x1
UP = 0x0


mousebtn = {
    "BTN_LEFT": MOUSE_BTN_LEFT,
    "BTN_RIGHT": MOUSE_BTN_RIGHT,
    "BTN_MIDDLE": MOUSE_BTN_MIDDLE,

}
mousecodemap = [
    None,
    mousebtn['BTN_LEFT'],
    mousebtn['BTN_MIDDLE'],
    mousebtn['BTN_RIGHT'],
    None,
    None,
    None,
    None,
]


def pack_events(events, name):
    buffer = (len(events)).to_bytes(1, 'little', signed=False)
    for (type, code, value) in events:
        buffer += struct.pack('<HHi', type, code, value)
    buffer += name.encode()
    return buffer


def unpack_events(buffer):
    print(buffer)
    length = buffer[0]
    events = [
        struct.unpack('<HHi', buffer[i*8+1:i*8+9])
        for i in range(length)
    ]
    name = buffer[length*8+1:].decode()
    return events, name


class sender:
    def __init__(self, addr) -> None:
        print("send all events to :", addr)
        self.targetIp = addr.split(":")[0]
        self.targetPort = int(addr.split(":")[1])
        self.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendArr = (self.targetIp, self.targetPort)

    def sendKey(self, scancode:int, downup):
        if downup == DOWN:
            kb.key_press(scancode.to_bytes(1, 'big'))
        else:
            kb.key_release(scancode.to_bytes(1, 'big'))

    def sendMouseMove(self, x=0, y=0):
        mouse.move(x,y)

    def sendMouseBTN(self, btn, downup):
        if btn <= 7 and mousecodemap[btn] != None:
            print("MOUSE BTN", mousecodemap[btn], downup)
            if downup == DOWN:
                mouse.btn_press(mousecodemap[btn])
            else:
                mouse.btn_release(mousecodemap[btn])
    def sendWheel(self, value):
        print("WHEEL", value)
        mouse.wheel_move(value)


if __name__ == "__main__":
    addr = "192.168.3.104:61069"
    if os.path.exists("./addr.txt"):
        with open("./addr.txt", "r") as f:
            addr = f.read()
    senderInstance = sender(addr)
    pygame.init()
    screen = pygame.display.set_mode((320, 240), 0, 32)
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == QUIT:
                flag = False
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pass
                    # flag = False
                    # break
                senderInstance.sendKey(event.scancode, DOWN)
            elif event.type == KEYUP:
                senderInstance.sendKey(event.scancode, UP)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                senderInstance.sendMouseBTN(event.button, DOWN)
            elif event.type == pygame.MOUSEBUTTONUP:
                senderInstance.sendMouseBTN(event.button, UP)
            elif event.type == pygame.MOUSEMOTION:
                rel = pygame.mouse.get_rel()
                senderInstance.sendMouseMove(x=rel[0] , y=rel[1] )
            elif event.type == pygame.MOUSEWHEEL:
                senderInstance.sendWheel(event.y)
