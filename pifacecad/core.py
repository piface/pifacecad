from .lcd import PiFaceLCD
import pifacecommon


DEFAULT_SPI_BUS = 0
DEFAULT_SPI_CHIP_SELECT = 1
INPUT_PORT = pifacecommon.core.GPIOA
MAX_SWITCHES = 8


class NoPiFaceCADDetectedError(Exception):
    pass


class Switch(pifacecommon.core.DigitalInputItem):
    """A switch on PiFace CAD."""
    def __init__(self, switch_num, board_num=0):
        if switch_num < 0 or switch_num >= MAX_SWITCHES:
            raise pifacecommon.core.RangeError(
                "Specified switch index (%d) out of range." % switch_num)
        else:
            super(Switch, self).__init__(
                switch_num, INPUT_PORT, board_num, toggle_mask=1)


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
        self.switch_port = pifacecommon.core.DigitalInputPort(
            INPUT_PORT, board_num, toggle_mask=0xff)
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


def init(init_board=True,
         bus=DEFAULT_SPI_BUS,
         chip_select=DEFAULT_SPI_CHIP_SELECT):
    """Initialises the PiFace CAD board.

    :param init_board: Initialise the board (default: True)
    :type init_board: boolean
    :param bus: SPI bus /dev/spidev<bus>.<chipselect> (default: {bus})
    :type bus: int
    :param chip_select: SPI bus /dev/spidev<bus>.<chipselect> (default: {chip})
    :type chip_select: int
    :raises: :class:`NoPiFaceDigitalDetectedError`
    """.format(bus=DEFAULT_SPI_BUS, chip=DEFAULT_SPI_CHIP_SELECT)

    pifacecommon.core.init(bus, chip_select)

    if not init_board:
        return

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
    pfioconf = pifacecommon.core.read(pifacecommon.core.IOCON)
    if pfioconf != ioconfig:
        raise NoPiFaceCADDetectedError(
            "No PiFace Control and Display board detected!")

    pifacecommon.core.write(0xFF, pifacecommon.core.IODIRA)  # port A as inputs
    pifacecommon.core.write(0xFF, pifacecommon.core.GPPUA)  # turn on pullups
    pifacecommon.core.write(0, pifacecommon.core.IODIRB)  # port B as outputs
    pifacecommon.interrupts.enable_interrupts(INPUT_PORT)


def deinit():
    """Deitialises the PiFace CAD board."""
    pifacecommon.interrupts.disable_interrupts(INPUT_PORT)
    pifacecommon.core.deinit()
