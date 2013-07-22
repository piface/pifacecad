import pifacecommon
import pifacecad


class LCDQuestion(object):
    """Asks a question on the LCD"""
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

    def ask(self):
        """Asks the question using the LCD screen.
        Returns the index of the answer selected.
        Uses a new PiFacecad object (backlight on) if none provided.
        """
        self.cad.lcd.clear()
        self.cad.lcd.write(self.question)
        self.change_answer(self._displayed_answer_index)
        self.cad.lcd.display_on()

        # wait for user input
        ifm = pifacecommon.InputFunctionMap()

        def next_answer_switch_pressed(flag, byte):
            self.next_answer()
            return True

        def prev_answer_switch_pressed(flag, byte):
            self.previous_answer()
            return True

        def select_answer_switch_pressed(flag, byte):
            return False

        ifm.register(
            input_num=7,
            direction=pifacecommon.IN_EVENT_DIR_ON,
            callback=next_answer_switch_pressed
        )
        ifm.register(
            input_num=6,
            direction=pifacecommon.IN_EVENT_DIR_ON,
            callback=prev_answer_switch_pressed
        )
        ifm.register(
            input_num=5,
            direction=pifacecommon.IN_EVENT_DIR_ON,
            callback=select_answer_switch_pressed
        )
        pifacecad.wait_for_input(ifm)
        return self._displayed_answer_index

    def next_answer(self):
        answer_index = (self._displayed_answer_index + 1) % len(self.answers)
        self.change_answer(answer_index)

    def previous_answer(self):
        answer_index = (self._displayed_answer_index - 1) % len(self.answers)
        self.change_answer(answer_index)

    def change_answer(self, new_answer_index=None):
        if new_answer_index is None:
            new_answer_index = \
                (self._displayed_answer_index + 1) % len(self.answers)

        # pad with spaces to overwrite previous answer (ljust)
        prev_ans = self.answers[self._displayed_answer_index]
        prev_ans_len = max(len(prev_ans), pifacecad.LCD_WIDTH)
        answer = self.answers[new_answer_index].ljust(prev_ans_len)

        self.cad.lcd.set_cursor(0, 1)
        if self.selector is None:
            self.cad.lcd.write(answer)
        else:
            self.cad.lcd.write("%s%s" % (self.selector, answer))

        self._displayed_answer_index = new_answer_index
