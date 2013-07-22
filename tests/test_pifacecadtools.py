import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad
import pifacecad.tools

pifacecad.init()

# question
# ANSWERS = (
#     "Because I said so",
#     "Why not?",
#     "Maybe",
#     "42"
# )

# question = pifacecadtools.LCDQuestion(question="Why?", answers=ANSWERS)

# ans_index = question.ask()
# print("You selected '%s'" % ANSWERS[ans_index])

# scanf
cad = pifacecad.PiFaceCAD()
cad.lcd.set_cursor(1, 1)
try:
    scanner = pifacecad.tools.LCDScanf(
        format="%i%2m%i%r",
        custom_values=("a", "bb", "ccc"),
        cad=cad
    )
    x = scanner.scan()
except KeyboardInterrupt:
    print(":-(")
else:
    print(x)
