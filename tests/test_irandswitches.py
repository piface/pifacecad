# -*- coding: utf-8 -*-
import os
import sys
import threading
import multiprocessing
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecommon
import pifacecad


def input0(event):
    print("input 0 was pressed")


def input1(event):
    print("input 1 was pressed")


def input2(event):
    print("input 2 was pressed")


def input3(event):
    print("input 3 was pressed")


def ir1(event):
    print("ir 1 pressed")


def ir2(event):
    print("ir 2 pressed")


def ir3(event):
    print("ir 3 pressed")


def ir4(event):
    print("ir 4 pressed")

pifacecad.init()

sl = pifacecad.SwitchEventListener()
sl.register(0, pifacecad.IODIR_ON, input0)
sl.register(1, pifacecad.IODIR_ON, input1)
sl.register(2, pifacecad.IODIR_ON, input2)
sl.register(3, pifacecad.IODIR_ON, input3)

irl = pifacecad.IREventListener(
    prog="pifacecadtest", lircrc="./tests/testlircrc")
irl.register('1', ir1)
irl.register('2', ir2)
irl.register('3', ir3)
irl.register('4', ir4)

sl.activate()
irl.activate()
