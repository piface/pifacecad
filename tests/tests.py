#!/usr/bin/env python3
import os
import sys
import unittest
import threading
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecommon
import pifacecad


PY3 = sys.version_info.major >= 3
if not PY3:
    input = raw_input

    from time import sleep

    class Barrier(object):
        def __init__(self, n, timeout=None):
            self.count = 0
            self.n = n
            self.timeout = timeout

        def wait(self):
            self.count += 1
            while self.count < self.n:
                sleep(0.0001)

    threading.Barrier = Barrier


SWITCH_RANGE = 8


# @unittest.skip
class TestPiFaceCADSwitches(unittest.TestCase):
    """General use tests (not really in the spirit of unittesting)."""
    def setUp(self):
        self.cad = pifacecad.PiFaceCAD()

    def test_switches(self):
        for a, b in ((0, 7), (1, 6), (2, 5), (3, 4)):
            input(
                "Hold switch {a} and {b}, then press enter.".format(a=a, b=b))
            self.assertEqual(self.cad.switches[a].value, 1)
            self.assertEqual(self.cad.switches[a].value, 1)

            # and the switch port
            bit_pattern = (1 << a) ^ (1 << b)
            self.assertEqual(self.cad.switch_port.value, bit_pattern)
        # for i in range(SWITCH_RANGE):
        #     input(
        #         "Hold switch {}, then press enter.".format(i))
        #     self.assertEqual(self.cad.switches[i].value, 1)
        #     self.assertEqual(self.cad.switches[i].value, 1)

        #     # and the switch port
        #     bit_pattern = (1 << i)
        #     self.assertEqual(self.cad.switch_port.value, bit_pattern)


class TestInterrupts(unittest.TestCase):
    def setUp(self):
        self.barrier = threading.Barrier(2, timeout=5)
        self.test_passed = False
        self.direction = pifacecad.IODIR_ON
        self.listener = pifacecad.SwitchEventListener()
        self.listener.register(0, self.direction, self.interrupts_test_helper)

    def test_interrupt(self):
        self.listener.activate()
        print("Press switch 0")
        self.barrier.wait()
        self.assertTrue(self.test_passed)

    def interrupts_test_helper(self, event):
        self.assertEqual(event.interrupt_flag, 0x1)
        self.assertEqual(event.interrupt_capture, 0xfe)
        self.assertEqual(event.pin_num, 0)
        self.assertEqual(event.direction, self.direction)
        self.test_passed = True
        self.barrier.wait()

    def tearDown(self):
        self.listener.deactivate()


@unittest.skip
class TestIR(unittest.TestCase):
    def setUp(self):
        self.barrier = threading.Barrier(2, timeout=5)
        self.listener = pifacecad.IREventListener(
            prog="pifacecadtest",
            lircrc="./tests/testlircrc")
        self.listener.register('1', self.ir_test_helper)
        self.test_passed = False

    def test_interrupt(self):
        self.listener.activate()
        print("Press remote button 1")
        self.barrier.wait()
        self.assertTrue(self.test_passed)

    def ir_test_helper(self, event):
        self.assertEqual(event.ir_code, '1')
        self.test_passed = True
        self.barrier.wait()

    def tearDown(self):
        self.listener.deactivate()


# @unittest.skip
class TestLCD(unittest.TestCase):
    def setUp(self):
        self.cad = pifacecad.PiFaceCAD()

    def test_normal_display(self):
        message = "1234567890123456\nabcdefghijklmnop"
        self.cad.lcd.write(message)
        question = "Does the screen say:\n{}\n".format(message)
        self.assertTrue(yes_no_question(question))
        self.cad.lcd.clear()

    def test_backlight(self):
        self.cad.lcd.backlight_on()
        self.assertTrue(yes_no_question("Is the backlight on?"))
        self.cad.lcd.backlight_off()
        self.assertTrue(yes_no_question("Is the backlight off?"))

    def test_scroll(self):
        message = "0000000000000000A\n0000000000000000A"
        self.cad.lcd.write(message)
        self.cad.lcd.viewport_corner = 1
        shiftedmessage = message = "000000000000000A\n000000000000000A"
        question = "Does the screen say:\n{}\n".format(shiftedmessage)
        self.assertTrue(yes_no_question(question))
        self.cad.lcd.clear()

    def test_set_cursor(self):
        self.cad.lcd.set_cursor(15, 1)
        self.assertTrue(
            yes_no_question("Is the cursor at the bottom right corner?"))
        self.cad.lcd.home()


def yes_no_question(question):
    answer = input("{} [Y/n] ".format(question))
    correct_answers = ("y", "yes", "Y", "")
    return answer in correct_answers


if __name__ == "__main__":
    unittest.main()
