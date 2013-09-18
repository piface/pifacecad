# -*- coding: utf-8 -*-
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad


def input0(event):
    print("input 0 was pressed")


def input1(event):
    print("input 1 was pressed")


def input2(event):
    print("input 2 was pressed")


def input3(event):
    print("input 3 was pressed")


pifacecad.init()

sl = pifacecad.SwitchEventListener()
sl.register(0, pifacecad.IODIR_ON, input0)
sl.register(1, pifacecad.IODIR_ON, input1)
sl.register(2, pifacecad.IODIR_ON, input2)
sl.register(3, pifacecad.IODIR_ON, input3)

sl.activate()
