import os
import sys
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
import pifacecad
from pifacecad.tools.scanf import LCDScanf


if __name__ == '__main__':
    cad = pifacecad.PiFaceCAD()
    scanner = LCDScanf("Give c%2c i%2i 0x%3x %r")
    print(scanner.scan())
    cad.lcd.clear()
    input("Press enter.")
