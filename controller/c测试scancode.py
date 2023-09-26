import math
import threading
import time

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

from utils.defines import *
from utils.interface import *

kb = KeyBoard(r'/dev/hidg0')

duiying = [
    "KEY_LEFT_CTRL",
    "KEY_LEFT_SHIFT",
    "KEY_LEFT_ALT",
    "KEY_LEFT_GUI",
    "KEY_RIGHT_CTRL",
    "KEY_RIGHT_SHIFT",
    "KEY_RIGHT_ALT",
    "KEY_RIGHT_GUI",
    "KEY_A",
    "KEY_B",
    "KEY_C",
    "KEY_D",
    "KEY_E",
    "KEY_F",
    "KEY_G",
    "KEY_H",
    "KEY_I",
    "KEY_J",
    "KEY_K",
    "KEY_L",
    "KEY_M",
    "KEY_N",
    "KEY_O",
    "KEY_P",
    "KEY_Q",
    "KEY_R",
    "KEY_S",
    "KEY_T",
    "KEY_U",
    "KEY_V",
    "KEY_W",
    "KEY_X",
    "KEY_Y",
    "KEY_Z",
    "KEY_1",
    "KEY_2",
    "KEY_3",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_0",
    "KEY_RETURN",
    "KEY_ENTER",
    "KEY_ESC",
    "KEY_ESCAPE",
    "KEY_BCKSPC",
    "KEY_BACKSPACE",
    "KEY_TAB",
    "KEY_SPACE",
    "KEY_MINUS",
    "KEY_DASH",
    "KEY_EQUALS",
    "KEY_EQUAL",
    "KEY_LBRACKET",
    "KEY_RBRACKET",
    "KEY_BACKSLASH",
    "KEY_HASH",
    "KEY_NUMBER",
    "KEY_SEMICOLON",
    "KEY_QUOTE",
    "KEY_BACKQUOTE",
    "KEY_TILDE",
    "KEY_COMMA",
    "KEY_PERIOD",
    "KEY_STOP",
    "KEY_SLASH",
    "KEY_CAPS_LOCK",
    "KEY_CAPSLOCK",
    "KEY_F1",
    "KEY_F2",
    "KEY_F3",
    "KEY_F4",
    "KEY_F5",
    "KEY_F6",
    "KEY_F7",
    "KEY_F8",
    "KEY_F9",
    "KEY_F10",
    "KEY_F11",
    "KEY_F12",
    "KEY_PRINT",
    "KEY_SCROLL_LOCK",
    "KEY_SCROLLLOCK",
    "KEY_PAUSE",
    "KEY_INSERT",
    "KEY_HOME",
    "KEY_PAGEUP",
    "KEY_PGUP",
    "KEY_DEL",
    "KEY_DELETE",
    "KEY_END",
    "KEY_PAGEDOWN",
    "KEY_PGDOWN",
    "KEY_RIGHT",
    "KEY_LEFT",
    "KEY_DOWN",
    "KEY_UP",
    "KEY_NUM_LOCK",
    "KEY_NUMLOCK",
    "KEY_KP_DIVIDE",
    "KEY_KP_MULTIPLY",
    "KEY_KP_MINUS",
    "KEY_KP_PLUS",
    "KEY_KP_ENTER",
    "KEY_KP_RETURN",
    "KEY_KP_1",
    "KEY_KP_2",
    "KEY_KP_3",
    "KEY_KP_4",
    "KEY_KP_5",
    "KEY_KP_6",
    "KEY_KP_7",
    "KEY_KP_8",
    "KEY_KP_9",
    "KEY_KP_0",
    "KEY_KP_PERIOD",
    "KEY_KP_STOP",
    "KEY_APPLICATION",
    "KEY_POWER",
    "KEY_KP_EQUALS",
    "KEY_KP_EQUAL",
    "KEY_F13",
    "KEY_F14",
    "KEY_F15",
    "KEY_F16",
    "KEY_F17",
    "KEY_F18",
    "KEY_F19",
    "KEY_F20",
    "KEY_F21",
    "KEY_F22",
    "KEY_F23",
    "KEY_F24",
    "KEY_EXECUTE",
    "KEY_HELP",
    "KEY_MENU",
    "KEY_SELECT",
    "KEY_CANCEL",
    "KEY_REDO",
    "KEY_UNDO",
    "KEY_CUT",
    "KEY_COPY",
    "KEY_PASTE",
    "KEY_FIND",
    "KEY_MUTE",
    "KEY_VOLUME_UP",
    "KEY_VOLUME_DOWN",
]

codes = [
    KEY_LEFT_CTRL,
    KEY_LEFT_SHIFT,
    KEY_LEFT_ALT,
    KEY_LEFT_GUI,
    KEY_RIGHT_CTRL,
    KEY_RIGHT_SHIFT,
    KEY_RIGHT_ALT,
    KEY_RIGHT_GUI,
    KEY_A,
    KEY_B,
    KEY_C,
    KEY_D,
    KEY_E,
    KEY_F,
    KEY_G,
    KEY_H,
    KEY_I,
    KEY_J,
    KEY_K,
    KEY_L,
    KEY_M,
    KEY_N,
    KEY_O,
    KEY_P,
    KEY_Q,
    KEY_R,
    KEY_S,
    KEY_T,
    KEY_U,
    KEY_V,
    KEY_W,
    KEY_X,
    KEY_Y,
    KEY_Z,
    KEY_1,
    KEY_2,
    KEY_3,
    KEY_4,
    KEY_5,
    KEY_6,
    KEY_7,
    KEY_8,
    KEY_9,
    KEY_0,
    KEY_RETURN,
    KEY_ENTER,
    KEY_ESC,
    KEY_ESCAPE,
    KEY_BCKSPC,
    KEY_BACKSPACE,
    KEY_TAB,
    KEY_SPACE,
    KEY_MINUS,
    KEY_DASH,
    KEY_EQUALS,
    KEY_EQUAL,
    KEY_LBRACKET,
    KEY_RBRACKET,
    KEY_BACKSLASH,
    KEY_HASH,
    KEY_NUMBER,
    KEY_SEMICOLON,
    KEY_QUOTE,
    KEY_BACKQUOTE,
    KEY_TILDE,
    KEY_COMMA,
    KEY_PERIOD,
    KEY_STOP,
    KEY_SLASH,
    KEY_CAPS_LOCK,
    KEY_CAPSLOCK,
    KEY_F1,
    KEY_F2,
    KEY_F3,
    KEY_F4,
    KEY_F5,
    KEY_F6,
    KEY_F7,
    KEY_F8,
    KEY_F9,
    KEY_F10,
    KEY_F11,
    KEY_F12,
    KEY_PRINT,
    KEY_SCROLL_LOCK,
    KEY_SCROLLLOCK,
    KEY_PAUSE,
    KEY_INSERT,
    KEY_HOME,
    KEY_PAGEUP,
    KEY_PGUP,
    KEY_DEL,
    KEY_DELETE,
    KEY_END,
    KEY_PAGEDOWN,
    KEY_PGDOWN,
    KEY_RIGHT,
    KEY_LEFT,
    KEY_DOWN,
    KEY_UP,
    KEY_NUM_LOCK,
    KEY_NUMLOCK,
    KEY_KP_DIVIDE,
    KEY_KP_MULTIPLY,
    KEY_KP_MINUS,
    KEY_KP_PLUS,
    KEY_KP_ENTER,
    KEY_KP_RETURN,
    KEY_KP_1,
    KEY_KP_2,
    KEY_KP_3,
    KEY_KP_4,
    KEY_KP_5,
    KEY_KP_6,
    KEY_KP_7,
    KEY_KP_8,
    KEY_KP_9,
    KEY_KP_0,
    KEY_KP_PERIOD,
    KEY_KP_STOP,
    KEY_APPLICATION,
    KEY_POWER,
    KEY_KP_EQUALS,
    KEY_KP_EQUAL,
    KEY_F13,
    KEY_F14,
    KEY_F15,
    KEY_F16,
    KEY_F17,
    KEY_F18,
    KEY_F19,
    KEY_F20,
    KEY_F21,
    KEY_F22,
    KEY_F23,
    KEY_F24,
    KEY_EXECUTE,
    KEY_HELP,
    KEY_MENU,
    KEY_SELECT,
    KEY_CANCEL,
    KEY_REDO,
    KEY_UNDO,
    KEY_CUT,
    KEY_COPY,
    KEY_PASTE,
    KEY_FIND,
    KEY_MUTE,
    KEY_VOLUME_UP,
    KEY_VOLUME_DOWN,
]



sendlist = []
recvlist = []

class SimpleEcho(WebSocket):
    def handleMessage(self):
        print("Message received", self.data)
        recvlist.append([self.data,time.time()])
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


server = SimpleWebSocketServer('', 8000, SimpleEcho)
threading.Thread(target=server.serveforever).start()


import socket

udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(("", 8001))


def udprecv():
    while True:
        recvData = udpSocket.recvfrom(100)
        content, destInfo = recvData
        recvlist.append([int(content.decode("utf-8")),time.time()])

threading.Thread(target=udprecv).start()



time.sleep(4)
for key in codes:
    print(hex(int.from_bytes(key, 'big')))
    kb.key_press(key)
    sendlist.append([key,time.time()])
    time.sleep(0.01)
    kb.key_release(key)
    time.sleep(0.2)



for key,time in sendlist:
    tojs = -1
    for refkey,reftime in recvlist:
        if abs( reftime - time) < 0.1:
            # print(hex(int.from_bytes(key, 'big')),refkey,reftime-time)
            tojs = refkey
    if tojs == -1:
        print('[{},null],'.format(int.from_bytes(key, 'big')))
    else:
        print('[{},{}],'.format(int.from_bytes(key, 'big'),tojs))
        
