"""
pifacecad.py
Provides I/O methods for interfacing with the RaspberryPi human interface
Copyright (C) 2013 thomasmarkpreston@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from pifacecommon.interrupts import (
    IODIR_FALLING_EDGE,
    IODIR_RISING_EDGE,
    IODIR_ON,
    IODIR_OFF,
    IODIR_BOTH,
)

from .core import (
    DEFAULT_SPI_BUS,
    DEFAULT_SPI_CHIP_SELECT,
    NUM_SWITCHES,
)

# classes
from .core import (
    PiFaceCAD,
    SwitchEventListener,
)

from .lcd import (
    PiFaceLCD,
    LCDBitmap,
)

from .ir import (
    IREventListener,
)
