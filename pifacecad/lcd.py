import math
import time
import pifacecommon.mcp23s17


# mcp23s17 GPIOB to HD44780 pin map
PH_PIN_D4 = 0
PH_PIN_D5 = 1
PH_PIN_D6 = 2
PH_PIN_D7 = 3
PH_PIN_ENABLE = 4
PH_PIN_RW = 5
PH_PIN_RS = 6
PH_PIN_LED_EN = 7

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80
LCD_NEWLINE = 0xC0

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

ROW_OFFSETS = [0x00, 0x40, 0x14, 0x54]

LCD_MAX_LINES = 2
LCD_WIDTH = 16
LCD_RAM_WIDTH = 80

# \ 1M for microseconds
PULSE_DELAY = 0.45 / float(1000000)  # 1us - pulse width must be > 450ns
SETTLE_DELAY = 37 / float(1000000)  # commands need 37us to settle
CLEAR_DISPLAY_DELAY = 3000 / float(1000000)

MAX_CUSTOM_BITMAPS = 8


class HD44780DataPort(pifacecommon.mcp23s17.MCP23S17RegisterNibble):
    """Data Port for an HD44780 LCD display. Must have the following
    properties:

        - value

    """
    def __init__(self, chip):
        super(HD44780DataPort, self).__init__(
            pifacecommon.mcp23s17.LOWER_NIBBLE,
            pifacecommon.mcp23s17.GPIOB,
            chip)


class HD44780ControlPort(pifacecommon.mcp23s17.MCP23S17Register):
    """Control Port for an HD44780 LCD display. Must have the following
    properties:

        - backlight_pin
        - read_write_pin
        - register_select_pin
        - enable_pin

    """
    def __init__(self, chip):
        super(HD44780ControlPort, self).__init__(
            pifacecommon.mcp23s17.GPIOB, chip)

    @property
    def backlight_pin(self):
        return self.bits[PH_PIN_LED_EN]

    @property
    def read_write_pin(self):
        return self.bits[PH_PIN_RW]

    @property
    def register_select_pin(self):
        return self.bits[PH_PIN_RS]

    @property
    def enable_pin(self):
        return self.bits[PH_PIN_ENABLE]


class HD44780LCD4bitModeMixIn(object):
    def send_byte(self, b):
        """Send byte to LCD. Each nibble is sent individually followed by a
        clock pulse because we're in 4 bit mode.

        :param b: The byte to send.
        :type b: int
        """
        self.data_port.value = (b >> 4) & 0xF
        self.pulse_clock()
        self.data_port.value = b & 0xF
        self.pulse_clock()

    def _pre_init_sequence(self):
        # init sequence from p.46 of datasheet.
        # https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
        time.sleep(0.015)
        self.data_port.value = 0x3
        self.pulse_clock()

        time.sleep(0.0041)
        self.data_port.value = 0x3
        self.pulse_clock()

        time.sleep(0.0001)
        self.data_port.value = 0x3
        self.pulse_clock()

        self.data_port.value = 0x2
        self.pulse_clock()


class HD44780LCD8bitModeMixIn(object):
    def send_byte(self, b):
        """Send byte to LCD. *I've not tested this!*

        :param b: The byte to send.
        :type b: int
        """
        self.data_port.value = b
        self.pulse_clock()

    def _pre_init_sequence(self):
        # init sequence from p.45 of datasheet.
        # https://www.sparkfun.com/datasheets/LCD/HD44780.pdf
        time.sleep(0.015)
        self.data_port.value = 0x30
        self.pulse_clock()

        time.sleep(0.0041)
        self.data_port.value = 0x30
        self.pulse_clock()

        time.sleep(0.0001)
        self.data_port.value = 0x30
        self.pulse_clock()

        self.data_port.value = 0x20
        self.pulse_clock()


class HD44780LCD(object):
    """Component part of an HD4780, must be combined with a 4 or 8 bit mixin.
    """
    def __init__(self, control_port, data_port, init_lcd=True):
        self.control_port = control_port
        self.data_port = data_port

        self._cursor_position = [0, 0]
        self._viewport_corner = 0  # top left corner

        self.numrows = LCD_MAX_LINES
        self.numcols = LCD_RAM_WIDTH

        self.displaycontrol = 0
        self.displayfunction = 0
        self.displaymode = 0

        if init_lcd:
            self._pre_init_sequence()  # either 4 bit or 8 bit mode
            self._init_sequence()
            self.displaycontrol = LCD_DISPLAYON | LCD_CURSORON | LCD_BLINKON
            self.update_display_control()

    def _init_sequence(self):
        self.displayfunction = LCD_4BITMODE | LCD_2LINE | LCD_5x8DOTS
        self.update_function_set()

        self.displaycontrol = LCD_DISPLAYOFF
        self.update_display_control()

        self.clear()

        self.displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
        self.update_entry_mode()

    @property
    def viewport_corner(self):
        """The top left corner of the current viewport."""
        return self._viewport_corner

    @viewport_corner.setter
    def viewport_corner(self, position):
        delta = position - self._viewport_corner
        if delta > 0:
            for i in range(delta):
                self.move_left()
        elif delta < 0:
            for i in range(abs(delta)):
                self.move_right()
        self._viewport_corner = position

    def see_cursor(self, col=None):
        """Moves the viewport so that the cursor is visible."""
        if col is None:
            col, row = self.get_cursor()

        # if off screen, move screen
        if col < self.viewport_corner:
            self.viewport_corner = col
        elif col > (self.viewport_corner + LCD_WIDTH - 1):
            self.viewport_corner = col - (LCD_WIDTH - 1)

    def clear(self):
        """Clears the display."""
        self.send_command(LCD_CLEARDISPLAY)  # command to clear display
        # clearing the display takes a long time
        time.sleep(CLEAR_DISPLAY_DELAY)
        self._cursor_position = [0, 0]
        self._viewport_corner = 0

    def home(self):
        """Moves the cursor to the home position."""
        self.send_command(LCD_RETURNHOME)  # set cursor position to zero
        time.sleep(CLEAR_DISPLAY_DELAY)
        self._cursor_position = [0, 0]
        self._viewport_corner = 0

    # entry mode set
    def update_entry_mode(self):
        """Update entrymodeset to reflect the displaymode."""
        self.send_command(LCD_ENTRYMODESET | self.displaymode)

    def left_to_right(self):
        """Sets the text to flow from left to right."""
        self.displaymode |= LCD_ENTRYLEFT
        self.update_entry_mode()

    def right_to_left(self):
        """Sets the text to flow from right to left."""
        self.displaymode &= ~LCD_ENTRYLEFT
        self.update_entry_mode()

    def right_justify(self):
        """Right justifies text from the cursor."""
        self.displaymode |= LCD_ENTRYSHIFTINCREMENT
        self.update_entry_mode()

    def left_justify(self):
        """Left justifies text from the cursor."""
        self.displaymode &= ~LCD_ENTRYSHIFTINCREMENT
        self.update_entry_mode()

    # display control
    def update_display_control(self):
        """Update the display control to reflect the displaycontrol."""
        self.send_command(LCD_DISPLAYCONTROL | self.displaycontrol)

    def display_off(self):
        """Turns the display off (quickly)."""
        self.displaycontrol &= ~LCD_DISPLAYON
        self.update_display_control()

    def display_on(self):
        """Turns the display on (quickly)."""
        self.displaycontrol |= LCD_DISPLAYON
        self.update_display_control()

    def cursor_off(self):
        """Turns the underline cursor off."""
        self.displaycontrol &= ~LCD_CURSORON
        self.update_display_control()

    def cursor_on(self):
        """Turns the underline cursor on."""
        self.displaycontrol |= LCD_CURSORON
        self.update_display_control()

    def blink_off(self):
        """Turns off the blinking cursor."""
        self.displaycontrol &= ~LCD_BLINKON
        self.update_display_control()

    def blink_on(self):
        """Turns on the blinking cursor."""
        self.displaycontrol |= LCD_BLINKON
        self.update_display_control()

    # cursor or display shift
    def move_left(self):
        """Scrolls the display without changing the RAM."""
        self.send_command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)
        self._viewport_corner += 1

    def move_right(self):
        """Scrolls the display without changing the RAM."""
        self.send_command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)
        self._viewport_corner -= 1

    # function set
    def update_function_set(self):
        """Updates the function set to reflect the current displayfunction."""
        self.send_command(LCD_FUNCTIONSET | self.displayfunction)

    # cgram address set
    def set_cgram_address(self, address=0):
        """Start using CGRAM at the given address.

        :param address: The address to start at (default: 0)
        :type address: int
        """
        self.send_command(LCD_SETCGRAMADDR | address)

    # ddram address set
    def set_ddram_address(self, address=None):
        """Start using DDRAM at the given address.

        :param address: The address to start at (default: current)
        :type address: int
        """
        if address is None:
            col, row = self.get_cursor()
            address = self.colrow2address(col, row)
        self.send_command(LCD_SETDDRAMADDR | address)

    def set_cursor(self, col, row):
        """Places the cursor at the specified column and row.

        :param col: The column.
        :type col: int
        :param row: The row.
        :type row: int
        """
        if col == 0 and row == 1:
            self.send_command(LCD_NEWLINE)
        else:
            col = max(0, min(col, self.numcols - 1))
            row = max(0, min(row, self.numrows - 1))
            self.set_ddram_address(self.colrow2address(col, row))
        self._cursor_position = [col, row]

    def get_cursor(self):
        """Returns the current column and row of the cursor. Also fixes
        internal value.

        :returns: (int, int) -- A tuple containing the column and row.
        """
        fixed_col = self._cursor_position[0] % LCD_RAM_WIDTH
        fixed_row = self._cursor_position[1] + \
            math.floor(self._cursor_position[0] / LCD_RAM_WIDTH)

        self._cursor_position[0] = fixed_col
        self._cursor_position[1] = fixed_row

        return (fixed_col, fixed_row)

    def colrow2address(self, col, row):
        """Returns address of column and row.

        :param col: The column.
        :param col: int
        :param row: The row.
        :param row: int
        :returns: The address of the column and row.
        """
        return col + ROW_OFFSETS[int(row)]

    # backlight
    def backlight_on(self):
        """Turn on the backlight."""
        self.control_port.backlight_pin.value = 1

    def backlight_off(self):
        """Turn on the backlight."""
        self.control_port.backlight_pin.value = 0

    # send commands/characters
    def send_command(self, command):
        """Send command byte to LCD.

        :param command: The command byte to be sent.
        :type command: int
        """
        self.control_port.register_select_pin.value = 0
        self.send_byte(command)
        time.sleep(SETTLE_DELAY)

    def send_data(self, data):
        """Send data byte to LCD.

        :param data: The data byte to be sent.
        :type data: int
        """
        self.control_port.register_select_pin.value = 1
        self.send_byte(data)
        time.sleep(SETTLE_DELAY)

    def pulse_clock(self):
        """Pulse the LCD clock for reading data."""
        self.control_port.enable_pin.value = 1
        time.sleep(PULSE_DELAY)
        self.control_port.enable_pin.value = 0
        time.sleep(PULSE_DELAY)

    def write(self, text):
        """Writes a string to the LCD screen.

        :param text: The text that will be written.
        :type text: string
        """
        self.set_ddram_address()
        for char in text:
            if '\n' in char:
                self.set_cursor(0, 1)
            else:
                self.send_data(ord(char))
                self._cursor_position[0] += 1  # LCD auto increments

    def write_custom_bitmap(self, char_bank, bitmap=None):
        """Writes the custom bitmap in CGRAM stored at char_bank. If a
        LCDBitmap is given, store it in the CGRAM address char_bank and then
        write it to the screen.

        :param char_bank: The bitmap bank to write the bitmap from
            (max: {max_custom_bitmaps})
        :type char_bank: int
        :param bitmap: The bitmap to store in the CGRAM address and write.
        :type bitmap: :class:`LCDBitmap`
        """.format(max_custom_bitmaps=MAX_CUSTOM_BITMAPS)

        self.char_bank_in_range_or_error(char_bank)
        if bitmap is not None:
            self.store_custom_bitmap(char_bank, bitmap)
        col, row = self.get_cursor()  # start using the correct ddram address
        self.set_cursor(col, row)
        self.send_data(char_bank)
        self._cursor_position[0] += 1  # LCD auto increments

    def store_custom_bitmap(self, char_bank, bitmap):
        """Stores a custom bitmap bitmap at char_bank.

        :param char_bank: The CGRAM address to use.
        :type char_bank: int
        :param bitmap: The bitmap to store.
        :type bitmap: :class:`LCDBitmap`
        """
        self.char_bank_in_range_or_error(char_bank)
        self.set_cgram_address(char_bank*8)
        for line in bitmap:
            self.send_data(line)

    def char_bank_in_range_or_error(self, char_bank):
        """Raises an exception if char_bank is out of bounds. Returns True
        otherwise.

        :param char_bank: The address to check.
        :type char_bank: int
        """
        if char_bank >= MAX_CUSTOM_BITMAPS or \
                char_bank < 0:
            raise Exception(
                "There are only {max} custom characters (You tried to access "
                "{cgramaddr}).".format(
                    max=MAX_CUSTOM_BITMAPS,
                    cgramaddr=char_bank,
                )
            )
        else:
            return True


class LCDBitmap(bytearray):
    """A custom bitmap for the LCD screen."""
    # TODO: More efficiend to store this sideways (LCDchar: 5x8, Bitmap: 8x...)
    def __init__(self, lines=list()):
        super(LCDBitmap, self).__init__(self)
        for line in lines:
            self.append(line)


class PiFaceLCD(HD44780LCD, HD44780LCD4bitModeMixIn):
    """An HD44780 LCD in 4-bit mode."""
    pass
