# gen bitmaps with: http://www.quinapalus.com/hd44780udg.html
# import sys
# import os
# sys.path.insert(0, os.path.abspath('..'))
import time

import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad


batt_char = pifacecad.LCDBitmap(
    [0x0E, 0x1B, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F]
)
checkerboard = pifacecad.LCDBitmap(
    [0x15, 0xa, 0x15, 0xa, 0x15, 0xa, 0x15, 0xa]
)

left_holder = pifacecad.LCDBitmap(
    [0x3, 0xc, 0x8, 0x10, 0x10, 0x8, 0xc, 0x3]
)
right_holder = pifacecad.LCDBitmap(
    [0x18, 0x6, 0x2, 0x1, 0x1, 0x2, 0x6, 0x18]
)
middle_holder = pifacecad.LCDBitmap(
    [0x1f, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f]
)
left_heart = pifacecad.LCDBitmap(
    [0x6, 0xf, 0x1f, 0xf, 0xf, 0x7, 0x3, 0x1]
)
right_heart = pifacecad.LCDBitmap(
    [0xc, 0x1e, 0x1f, 0x1f, 0x1e, 0x1c, 0x18, 0x10]
)

loading = list()
loading.append(pifacecad.LCDBitmap(
    [0x1f, 0x11, 0xa, 0x4, 0x4, 0xa, 0x11, 0x1f]
))
loading.append(pifacecad.LCDBitmap(
    [0x1f, 0x11, 0xa, 0x4, 0x4, 0xa, 0x1f, 0x1f]
))
loading.append(pifacecad.LCDBitmap(
    [0x1f, 0x11, 0xa, 0x4, 0x4, 0xe, 0x1f, 0x1f]
))
loading.append(pifacecad.LCDBitmap(
    [0x1f, 0x11, 0xe, 0x4, 0x4, 0xe, 0x1f, 0x1f]
))
loading.append(pifacecad.LCDBitmap(
    [0x1f, 0x1f, 0xe, 0x4, 0x4, 0xe, 0x1f, 0x1f]
))


print("Creating PiFaceCAD object")
pc = pifacecad.PiFaceCAD()

print("Storing")
pc.lcd.store_custom_bitmap(0, batt_char)
pc.lcd.store_custom_bitmap(1, checkerboard)
pc.lcd.store_custom_bitmap(2, left_holder)
pc.lcd.store_custom_bitmap(3, middle_holder)
pc.lcd.store_custom_bitmap(4, right_holder)
pc.lcd.store_custom_bitmap(5, left_heart)
pc.lcd.store_custom_bitmap(6, right_heart)

print("Printing")
pc.lcd.write("abc")
for i in range(7):
    pc.lcd.write_custom_bitmap(i)
#pc.lcd.write("def")

input("next? (press enter")
#pc.lcd.clear()
pc.lcd.blink_off()
pc.lcd.cursor_off()
# loading
for i in range(len(loading)):
    pc.lcd.store_custom_bitmap(i, loading[i])

# i = 0
# while True:
#     i = (i + 1) % len(loading)
#     pc.lcd.write_custom_bitmap(i)
#     pc.lcd.home()
#     time.sleep(1)
