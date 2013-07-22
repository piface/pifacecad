# -*- coding: utf-8 -*-
import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad


pifacecad.init()
pfcad = pifacecad.PiFaceCAD()


def turn_backlight_on(ircode):
    pfcad.lcd.backlight_on()
    return True


def turn_backlight_off(ircode):
    pfcad.lcd.backlight_off()
    return True


def write_message(test):
    pfcad.lcd.write("Hello, World!")
    return True


def exit(test):
    pfcad.lcd.clear()
    pfcad.lcd.write("exiting")
    return False


irfm = pifacecad.IRFunctionMap()
irfm.register(ir_code="1", callback=turn_backlight_on)
irfm.register(ir_code="2", callback=turn_backlight_off)
irfm.register(ir_code="3", callback=write_message)
irfm.register(ir_code="4", callback=exit)

pifacecad.wait_for_ir(
    ir_func_map=irfm,
    ir_config="./lircconf",
    prog="pifacecadtest",
)
