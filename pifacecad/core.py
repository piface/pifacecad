from .lcd import PiFaceLCD
import pifacecommon


SPI_BUS = 0
SPI_CHIP_SELECT = 1
INPUT_PORT = pifacecommon.core.GPIOA
MAX_SWITCHES = 8


class Switch(pifacecommon.core.DigitalInputItem):
    """A switch on PiFace CAD."""
    def __init__(self, switch_num, board_num=0):
        if switch_num < 0 or switch_num >= MAX_SWITCHES:
            raise pifacecommon.core.RangeError(
                "Specified switch index (%d) out of range." % switch_num)
        else:
            super(Switch, self).__init__(switch_num, INPUT_PORT, board_num)


class PiFaceCAD(object):
    """A PiFace Control and Display board.

    :attribute: board_num -- The board number.
    :attribute: switch_port -- See :class:`pifacecommon.core.DigitalInputPort`.
    :attribute: switches -- list containing :class:`Switch`.
    :attribute: lcd -- See :class:`pifacecad.lcd.PiFaceLCD`.

    Example:

    >>> cad = pifacecad.PiFaceCAD()
    >>> hex(cad.switch_port.value)
    0x02
    >>> cad.switches[1].value
    1
    >>> cad.lcd.write("Hello, PiFaceLCD!")
    >>> cad.lcd.backlight_on()
    """
    def __init__(self, board_num=0):
        self.board_num = board_num
        self.switch_port = \
            pifacecommon.core.DigitalInputPort(INPUT_PORT, board_num)
        self.switches = [Switch(i, board_num) for i in range(MAX_SWITCHES)]
        self.lcd = PiFaceLCD()


class SwitchEventListener(pifacecommon.interrupts.PortEventListener):
    """Listens for events on the switches and calls the mapped callback
    functions.

    >>> def print_flag(event):
    ...     print(event.interrupt_flag)
    ...
    >>> listener = pifacecad.SwitchEventListener()
    >>> listener.register(0, pifacecad.IODIR_ON, print_flag)
    >>> listener.activate()
    """
    def __init__(self):
        super(SwitchEventListener, self).__init__(INPUT_PORT)


def init():
    """Initialises the PiFace CAD board."""
    pifacecommon.core.init(SPI_BUS, SPI_CHIP_SELECT)
    ioconfig = (
        pifacecommon.core.BANK_OFF |
        pifacecommon.core.INT_MIRROR_OFF |
        pifacecommon.core.SEQOP_ON |
        pifacecommon.core.DISSLW_OFF |
        pifacecommon.core.HAEN_ON |
        pifacecommon.core.ODR_OFF |
        pifacecommon.core.INTPOL_LOW
    )
    pifacecommon.core.write(ioconfig, pifacecommon.core.IOCON)

    # set up port A as inputs and turn on the pullups, also enable interrupts
    pifacecommon.core.write(0xFF, pifacecommon.core.IODIRA)
    pifacecommon.core.write(0xFF, pifacecommon.core.GPPUA)

    ##### not needed?
    pifacecommon.core.write(0xFF, pifacecommon.core.GPINTENA)  # ????
    pifacecommon.core.read(INPUT_PORT)  # clear interrupt
    ##### not needed?

    # set port B as outputs
    pifacecommon.core.write(0, pifacecommon.core.IODIRB)


def deinit():
    """Deitialises the PiFace CAD board."""
    pifacecommon.core.deinit()
