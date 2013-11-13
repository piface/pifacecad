import sys
import threading
import pifacecad
import pifacecad.lcd

# Python 2 barrier hack (if you know a better way, please tell me)
PY3 = sys.version_info[0] >= 3
if not PY3:
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


class LCDQuestion(object):
    """Asks a question on the LCD"

    :param question: The question to be asked.
    :type question: string
    :param answers: The answers to choose from.
    :type answers: list
    :param selector: The selector displayed in front of each answer.
    :type selector: string
    :param cad: An already initialised PiFaceCAD object.
    :type cad: PiFaceCAD
    """
    def __init__(self, question, answers, selector=">", cad=None):
        self.question = question
        self.answers = answers
        self.selector = selector

        if cad is None:
            cad = pifacecad.PiFaceCAD()
            cad.lcd.backlight_on()
            cad.lcd.blink_off()
            cad.lcd.cursor_off()
            cad.lcd.display_off()  # don't want to see slow printing

        self.cad = cad

        self._displayed_answer_index = 0
        self.wait_for_return_string = None

    def ask(self):
        """Asks the question using the LCD screen.

        :returns: int -- index of the answer selected.
        """
        self.cad.lcd.clear()
        self.cad.lcd.write(self.question)
        self.change_answer(self._displayed_answer_index)
        self.cad.lcd.display_on()

        # wait for user input
        listener = pifacecad.SwitchEventListener(self.cad)
        listener.register(7, pifacecad.IODIR_ON, self.next_answer)
        listener.register(6, pifacecad.IODIR_ON, self.previous_answer)
        listener.register(5,
                          pifacecad.IODIR_ON,
                          self.select_answer_switch_pressed)

        self.wait_for_return_string = threading.Barrier(2)
        listener.activate()
        self.wait_for_return_string.wait()
        listener.deactivate()
        return self._displayed_answer_index

    def select_answer_switch_pressed(self, event):
        self.wait_for_return_string.wait()

    def next_answer(self, event=None):
        answer_index = (self._displayed_answer_index + 1) % len(self.answers)
        self.change_answer(answer_index)

    def previous_answer(self, event=None):
        answer_index = (self._displayed_answer_index - 1) % len(self.answers)
        self.change_answer(answer_index)

    def change_answer(self, new_answer_index=None):
        if new_answer_index is None:
            new_answer_index = \
                (self._displayed_answer_index + 1) % len(self.answers)

        # pad with spaces to overwrite previous answer (ljust)
        prev_ans = self.answers[self._displayed_answer_index]
        prev_ans_len = max(len(prev_ans), pifacecad.lcd.LCD_WIDTH)
        answer = self.answers[new_answer_index].ljust(prev_ans_len)

        self.cad.lcd.set_cursor(0, 1)
        if self.selector is None:
            self.cad.lcd.write(answer)
        else:
            self.cad.lcd.write("%s%s" % (self.selector, answer))

        self._displayed_answer_index = new_answer_index
