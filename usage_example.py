import math
import time

from utils.defines import *
from utils.interface import *

# kb = KeyBoard(r'/dev/hidg0')
# mouse = Mouse(r'/dev/hidg1')

kb = KeyBoard("192.168.3.104", 5643)
mouse = Mouse("192.168.3.104", 5644)


def makeCircle(r):
    points = []
    for i in range(r):
        x = r * math.cos(i * 2 * math.pi / r)
        y = r * math.sin(i * 2 * math.pi / r)
        points.append((int(x), int(y)))
    offsets = []
    for i in range(len(points)-1):
        x = points[i+1][0] - points[i][0]
        y = points[i+1][1] - points[i][1]
        offsets.append((x, y))
    return offsets


# # time.sleep(2)
# mouse.btn_press(MOUSE_BTN_LEFT)
# mouse.btn_release(MOUSE_BTN_LEFT)


# time.sleep(0.5)

# mouse.move(x=60, y=-60)


for i in range(10):
    for (x, y) in makeCircle(200):
        mouse.move(x=x, y=y)
        time.sleep(1/250)


# for i in range(10):
#     mouse.wheel_move(wh=-1)
#     time.sleep(0.5)

for key in [KEY_A,KEY_B,KEY_C,KEY_D]:
    kb.key_press(key)
    time.sleep(0.1)
    kb.key_release(key)
    time.sleep(0.1)

# for key in [KEY_LEFT_CTRL,
#             KEY_LEFT_SHIFT,
#             KEY_LEFT_ALT,
#             KEY_RIGHT_CTRL,
#             KEY_RIGHT_SHIFT,
#             KEY_RIGHT_ALT,
#             ]:
#     kb.key_press(key)
#     time.sleep(0.1)
#     kb.key_release(key)
#     time.sleep(0.5)
