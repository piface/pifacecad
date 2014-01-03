import os
import sys
import unittest
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad
import pifacecad.tools


class TestLCDScanf(unittest.TestCase):

    def setUp(self):
        self.cad = pifacecad.PiFaceCAD()
        self.cad.lcd.set_cursor(1, 1)

    def test_scanner(self):
        correct_answer = [2, "bc", "apple"]
        print("Enter", correct_answer)
        scanner = pifacecad.tools.LCDScanf(format="%i %2c %m%r",
                                           custom_values=("orange", "apple"),
                                           cad=self.cad)
        answer = scanner.scan()
        self.assertEqual(answer, correct_answer)

    def tearDown(self):
        self.cad.lcd.clear()


class TestLCDQuestion(unittest.TestCase):

    def test_question(self):
        correct_answer = "Why not?"
        print("Enter", correct_answer)

        question = pifacecad.tools.LCDQuestion
        the_answers = ("Because I said so",
                       "Why not?",
                       "Maybe",
                       "42")

        question = pifacecad.tools.LCDQuestion(question="Why?",
                                               answers=the_answers)
        answer_index = question.ask()
        self.assertEqual(answer_index, the_answers.index(correct_answer))


if __name__ == "__main__":
    unittest.main()
