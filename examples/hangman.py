#!/usr/bin/python3
import sys
from time import sleep
from random import randint
import pifacecad
import pifacecad.tools
from pifacecad.lcd import LCD_WIDTH


WORDS = ["piface", "raspberrypi", "horses", "eggs", "bacon"]

TOP_LEFT_INDEX, TOP_MIDDLE_INDEX, TOP_RIGHT_INDEX = range(3)
BOTTOM_LEFT_INDEX, BOTTOM_MIDDLE_INDEX, BOTTOM_RIGHT_INDEX = range(3, 6)

# hangman is in six squares
HANGMAN_WIDTH = 3
stages = [
    # stage 0
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x0, 0x0, 0x0, 0x0]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 1
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 2
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x4, 0x4, 0x4, 0x0, 0x0, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 3
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x1c, 0x4, 0x4, 0x0, 0x0, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 4
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x1f, 0x4, 0x4, 0x0, 0x0, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 5
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x1f, 0x4, 0x4, 0x8, 0x10, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
    # stage 6
    {
    'top-left': pifacecad.LCDBitmap(
        [0x0, 0x0, 0xf, 0x8, 0x8, 0x8, 0x8, 0x8]),
    'top-middle': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x1c, 0x4, 0x4, 0xe, 0xa, 0xe]),
    'top-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]),
    'bottom-left': pifacecad.LCDBitmap(
        [0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x8, 0x1f]),
    'bottom-middle': pifacecad.LCDBitmap(
        [0x1f, 0x4, 0x4, 0xa, 0x11, 0x0, 0x0, 0x1f]),
    'bottom-right': pifacecad.LCDBitmap(
        [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x18]),
    },
]


class HangmanIsDead(Exception):
    pass


class Hangman(object):
    def __init__(self, cad):
        self._stage = 0
        self.cad = cad
        self.cad.lcd.blink_off()
        self.cad.lcd.backlight_on()
        self.print_hangman()

    def print_hangman(self):
        self.cad.lcd.set_cursor(0, 0)
        self.cad.lcd.write_custom_bitmap(
            TOP_LEFT_INDEX, stages[self.stage]['top-left'])
        self.cad.lcd.write_custom_bitmap(
            TOP_MIDDLE_INDEX, stages[self.stage]['top-middle'])
        self.cad.lcd.write_custom_bitmap(
            TOP_RIGHT_INDEX, stages[self.stage]['top-right'])
        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write_custom_bitmap(
            BOTTOM_LEFT_INDEX, stages[self.stage]['bottom-left'])
        self.cad.lcd.write_custom_bitmap(
            BOTTOM_MIDDLE_INDEX, stages[self.stage]['bottom-middle'])
        self.cad.lcd.write_custom_bitmap(
            BOTTOM_RIGHT_INDEX, stages[self.stage]['bottom-right'])

    @property
    def stage(self):
        return self._stage

    @stage.setter
    def stage(self, new_stage):
        new_stage = min(new_stage, len(stages)-1)
        self._stage = new_stage
        self.print_hangman()
        if new_stage >= len(stages)-1:
            raise HangmanIsDead()


class HangmanGame(object):
    def __init__(self, word):
        self.cad = pifacecad.PiFaceCAD()
        self.hangman = Hangman(self.cad)
        self.word = word
        self.correct_guesses = list()

    def start(self):
        self.print_word()
        while True:
            letter = self.ask_for_letter()

            # if the user has already guessed this letter
            if letter in self.correct_guesses:
                try:
                    self.hangman.stage += 1
                    continue
                except HangmanIsDead:
                    self.say_gave_over()
                    break

            # if the letter is correct
            if letter in self.word:
                self.correct_guesses.append(letter)
            else:
                try:
                    self.hangman.stage += 1
                    continue
                except HangmanIsDead:
                    self.say_gave_over()
                    break

            self.print_word()

            if self.user_has_won():
                self.say_well_done()
                break

    def user_has_won(self):
        for c in self.word:
            if c in self.correct_guesses:
                continue
            else:
                return False
        else:
            return True

    def print_word(self):
        self.cad.lcd.set_cursor(3, 0)
        for c in self.word:
            if c in self.correct_guesses:
                self.cad.lcd.write(c)
            else:
                self.cad.lcd.write("_")

    def ask_for_letter(self):
        self.cad.lcd.set_cursor(3, 1)
        scanner = pifacecad.tools.LCDScanf(
            format="Guess: %c%r", cad=self.cad)
        return scanner.scan()[0]  # scan returns a list

    def say_well_done(self):
        print("Well done!")
        self.cad.lcd.set_cursor(3, 1)
        self.cad.lcd.write("Well done!".ljust(LCD_WIDTH-HANGMAN_WIDTH))

    def say_gave_over(self):
        print("GAME OVER!")
        self.cad.lcd.set_cursor(3, 1)
        self.cad.lcd.write("GAME OVER!".ljust(LCD_WIDTH-HANGMAN_WIDTH))


if __name__ == "__main__":
    try:
        word = sys.argv[1].lower()
    except IndexError:
        word = WORDS[randint(0, len(WORDS)-1)]
    game = HangmanGame(word)
    game.start()
