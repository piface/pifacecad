# -*- coding: utf-8 -*-
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad


def input_callback(event):
    print("input {} was pressed".format(event.pin_num))
    print(pifacecad.PiFaceCAD().switch_port.value)

pifacecad.init()

sl = pifacecad.SwitchEventListener()
for i in range(8):
    sl.register(i, pifacecad.IODIR_ON, input_callback)

sl.activate()
