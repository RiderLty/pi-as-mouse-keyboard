import os

from utils.defines import *


def setBit(value, index, bit):
    mask = 1 << index
    return (value & ~mask) if bit == 0 else (value | mask)


class Mouse:
    def __init__(self, path) -> None:
        self.fd = os.open(path, os.O_RDWR)
        self.btns = 0x00
        try:
            os.write(self.fd, b'\x00' * 5)
        except Exception as e:
            raise e

    def __del__(self):
        try:
            os.write(self.fd, b'\x00' * 5)
            os.close(self.fd)
        except Exception as e:
            pass

    def report(self, x=0, y=0, wh=0, l=None, r=None, m=None):
        self.btns = setBit(self.btns, MOUSE_BTN_LEFT, l) if l is not None else self.btns
        self.btns = setBit(self.btns, MOUSE_BTN_RIGHT, r) if r is not None else self.btns
        self.btns = setBit(self.btns, MOUSE_BTN_MIDDLE, m) if m is not None else self.btns
        write_bytes = (self.btns).to_bytes(1, byteorder='little', signed=False)
        write_bytes += (x).to_bytes(2, 'little', signed=True)
        write_bytes += (y).to_bytes(2, 'little', signed=True)
        write_bytes += (wh).to_bytes(2, 'little', signed=True)
        os.write(self.fd, write_bytes)

    def move(self, x=0, y=0):
        self.report(x=x, y=y)

    def btn_press(self, btn):
        if btn == MOUSE_BTN_LEFT:
            self.report(l=1)
        elif btn == MOUSE_BTN_RIGHT:
            self.report(r=1)
        elif btn == MOUSE_BTN_MIDDLE:
            self.report(m=1)

    def btn_release(self, btn):
        if btn == MOUSE_BTN_LEFT:
            self.report(l=0)
        elif btn == MOUSE_BTN_RIGHT:
            self.report(r=0)
        elif btn == MOUSE_BTN_MIDDLE:
            self.report(m=0)

    def wheel_move(self, wh=0):
        self.report(wh=wh)




class KeyBoard:
    def __init__(self, path):
        self.fd = os.open(path, os.O_RDWR)
        try:
            os.write(self.fd, b"\x00" * 8)
        except Exception as e:
            raise e
        self.spacialKey = 0x00
        self.special_key_order = [KEY_LEFT_CTRL, KEY_LEFT_SHIFT, KEY_LEFT_ALT,
                                  KEY_LEFT_GUI, KEY_RIGHT_CTRL, KEY_RIGHT_SHIFT, KEY_RIGHT_ALT, KEY_RIGHT_GUI]
        self.key_state = set()

    def __del__(self):
        try:
            os.write(self.fd, b"\x00" * 8)
            os.close(self.fd)
        except Exception as e:
            pass

    def report(self,):
        write_bytes = (self.spacialKey).to_bytes( 1, byteorder='little', signed=False)
        write_bytes += b'\x00'  # 保留
        for down_key in self.key_state:
            write_bytes += down_key
        for __ in range(6 - len(self.key_state)):
            write_bytes += b'\x00'
        os.write(self.fd, write_bytes)

    def key_press(self, key):
        if key in self.special_key_order:
            self.spacialKey = setBit(
                self.spacialKey, self.special_key_order.index(key), 1)
        else:
            if len(self.key_state) < 6:
                self.key_state.add(key)
            else:
                return
        self.report()

    def key_release(self, key):
        if key in self.special_key_order:
            self.spacialKey = setBit(
                self.spacialKey, self.special_key_order.index(key), 0)
        else:
            if key in self.key_state:
                self.key_state.remove(key)
            else:
                return
        self.report()
