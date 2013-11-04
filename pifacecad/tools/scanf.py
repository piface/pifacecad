import sys
import math
from abc import ABCMeta
import threading
import pifacecad


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


# charset from http://mil.ufl.edu/4744/docs/lcdmanual/charset.gif
LCD_RETURN_CHAR = chr(126)  # arrow
LCD_PUNC_CHARSET = [chr(x) for x in range(0x21, 0x30)] + \
    [chr(x) for x in range(0x3A, 0x41)] + \
    [chr(x) for x in range(0x5B, 0x61)] + \
    [chr(x) for x in range(0x7B, 0xFF)]

# character specifiers for LCDScanf (defined at bottom)
# VALUE_SELECTS = {}


class UnknownSpecifierError(Exception):
    pass


class LCDScanf(object):
    """Allows the user to input text using the LCD.

    To change mode from moving and editing press switch 5 (navigation switch
    *in*). Move the navigation switch side to side (switches 6 and 7) to
    change character.

    The available character set is specified using a format string similar to
    printf. Supported character specifiers are::

        c: Characters
        C: Capital Characters
        i: Integers
        d: Integers
        x: Hexadecimal
        X: Capital Hexadecimal
        .: Punctuation
        m: Custom (specifed by ``custom_values`` in init args)
        r: Return (switch 5 to submit string)

    You must prefix them with a ``%`` symbol and you can also specify a number
    argument. Each specifier is returned as an element in a list.

    For example:

        >>> scanner = pifacecad.tools.LCDScanf("Text: %c%2i%.%r")
        >>> print(scanner.scan())  # user enters things on PiFaceCAD
        ['a', '13', '!']

    You can also specify custom values:

        >>> scanner = pifacecad.tools.LCDScanf(
        ...     "Animal: %m%r",
        ...     custom_values=('cat', 'dog', 'fish')
        ... )
        >>> print(scanner.scan())
        ['fish']
    """
    class ScanfMode(object):
        select, edit = range(2)

    def __init__(self, format, custom_values=None, cad=None):
        if cad is None:
            cad = pifacecad.PiFaceCAD()
            cad.lcd.backlight_on()
            cad.lcd.cursor_on()
            cad.lcd.display_off()  # don't want to see slow printing
            self.custom_cad = False
        else:
            self.custom_cad = True

        self.start_offset = cad.lcd.get_cursor()
        self.cad = cad
        self.display_string = ValueSelectString(format, custom_values)
        self.mode = self.ScanfMode.select
        self.wait_for_return_string = None

    def __del__(self):
        if not self.custom_cad:
            self.cad.lcd.clear()
            self.cad.lcd.display_off()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, newmode):
        if newmode == self.ScanfMode.select:
            self.cad.lcd.blink_off()
        elif newmode == self.ScanfMode.edit:
            self.cad.lcd.blink_on()
        self._mode = newmode

    def scan(self):
        #self.cad.lcd.clear()
        self.cad.lcd.write(str(self.display_string))
        # set the cursor to a sensible position
        try:
            first_value_select_index = \
                self.display_string.instanceindex(ValueSelect)
        except TypeError:
            # nothing to select, show the string and return
            self.cad.lcd.display_on()
            return self.display_string.selected_values
        else:
            col = first_value_select_index + self.start_offset[0]
            row = self.start_offset[1]
            self.cad.lcd.set_cursor(col, row)
            self.cad.lcd.display_on()

        # wait for user input
        listener = pifacecad.SwitchEventListener(self.cad)
        listener.register(7, pifacecad.IODIR_ON, self.right_event)
        listener.register(6, pifacecad.IODIR_ON, self.left_event)
        listener.register(5, pifacecad.IODIR_ON, self.change_mode_event)
        listener.register(4, pifacecad.IODIR_ON, self.return_string_event)

        self.wait_for_return_string = threading.Barrier(2)
        listener.activate()
        self.wait_for_return_string.wait()
        listener.deactivate()
        return self.display_string.selected_values

    def right_event(self, event):
        if self.mode == self.ScanfMode.select:
            self.move_cursor_right()
        elif self.mode == self.ScanfMode.edit:
            self.increment_value()

    def left_event(self, event):
        if self.mode == self.ScanfMode.select:
            self.move_cursor_left()
        elif self.mode == self.ScanfMode.edit:
            self.decrement_value()

    def change_mode_event(self, event):
        col, row = self.cad.lcd.get_cursor()
        if isinstance(
                self.display_string.value_at(col-self.start_offset[0]),
                ReturnCharacter):
            self.return_string_event(event)
        elif self.mode == self.ScanfMode.select:
            self.mode = self.ScanfMode.edit
        elif self.mode == self.ScanfMode.edit:
            self.mode = self.ScanfMode.select

    def return_string_event(self, event):
        self.wait_for_return_string.wait()

    def move_cursor_right(self):
        """move cursor right, roll around string, scroll screen.
        Only place cursor on ValueSelect, ignore plain text.
        """
        # go to next column, if past string: roll around
        col, row = self.cad.lcd.get_cursor()
        value_index = col - self.start_offset[0]
        value_index = (value_index + 1) % len(str(self.display_string))

        # make sure we land on a ValueSelect
        while (not is_selectable_character(self.display_string, value_index)):
            value_index = (value_index + 1) % len(str(self.display_string))

        col = value_index + self.start_offset[0]
        self.cad.lcd.set_cursor(col, row)
        self.cad.lcd.see_cursor(col)

    def move_cursor_left(self):
        """move cursor left, roll around string, scroll screen.
        Only place cursor on ValueSelect, ignore plain text.
        """
        # go to prev column, if before string: roll around to end
        col, row = self.cad.lcd.get_cursor()
        value_index = col - self.start_offset[0]
        value_index = (value_index - 1) % len(str(self.display_string))

        # make sure we land on a ValueSelect
        while (not is_selectable_character(self.display_string, value_index)):
            value_index = (value_index - 1) % len(str(self.display_string))

        col = value_index + self.start_offset[0]
        self.cad.lcd.set_cursor(col, row)
        self.cad.lcd.see_cursor()

    def increment_value(self):
        col, row = self.cad.lcd.get_cursor()
        value_select = self.display_string.value_at(col-self.start_offset[0])
        value_select.increment_value()
        self.write_value(value_select, col, row)

    def decrement_value(self):
        col, row = self.cad.lcd.get_cursor()
        value_select = self.display_string.value_at(col-self.start_offset[0])
        value_select.decrement_value()
        self.write_value(value_select, col, row)

    def write_value(self, value_select, col, row):
        string = str(value_select.value).ljust(value_select.longest_len)
        self.cad.lcd.write(string)
        self.cad.lcd.set_cursor(col, row)


class ValueSelect(list):
    """A character in a specified range"""
    def __init__(self, values=list(), value_index=0):
        super(ValueSelect, self).__init__(values)
        self.value_index = value_index

    def __str__(self):
        """Returns the selected value instead of a stringified list.
        Values are space-padded to the max length value selector
        """
        return str(self.value).ljust(self.longest_len)

    @property
    def longest_len(self):
        """Return the length of the longest value in this list.
        Example::

            ValueSelect(["one", "two", "three"]).longest_len() == 5
        """
        return max([len(str(x)) for x in self])

    @property
    def value(self):
        if len(self) <= 0:
            return None
        else:
            return self[self.value_index]

    @value.setter
    def value(self, v):
        if len(self) <= 0:
            self.append(v)

        self.value_index = self.index(v)

    def increment_value(self):
        self.value_index = (self.value_index + 1) % len(self)

    def decrement_value(self):
        self.value_index = (self.value_index - 1) % len(self)


class CharacterValueSelect(ValueSelect):
    def __init__(self):
        super(CharacterValueSelect, self).__init__(
            [c for c in char_range("a", "z")])


class CapsCharacterValueSelect(ValueSelect):
    def __init__(self):
        super(CapsCharacterValueSelect, self).__init__(
            [c for c in char_range("A", "Z")])


class PunctuationValueSelect(ValueSelect):
    def __init__(self):
        super(PunctuationValueSelect, self).__init__(
            [p for p in LCD_PUNC_CHARSET])


class NumericValue(object):
    __metaclass__ = ABCMeta
    base = 10

    def __int__(self):
        try:
            return int(self.value, self.base)
        except TypeError:
            return int(self.value)


class IntegerValueSelect(ValueSelect, NumericValue):
    def __init__(self):
        super(IntegerValueSelect, self).__init__([i for i in range(10)])
        self.base = 10


class HexadecimalValueSelect(ValueSelect, NumericValue):
    def __init__(self):
        super(HexadecimalValueSelect, self).__init__(
            [numeric for numeric in range(10)] +
            [alpha for alpha in char_range('A', 'F')]
        )
        self.base = 16


class ReturnCharacter(ValueSelect):
    def __init__(self):
        super(ReturnCharacter, self).__init__()
        self.append(LCD_RETURN_CHAR)


class MultiValueSelect(list):
    """A list of ValueSelects representing a single value."""
    def __init__(self, multiplier, value_select, custom_values=None):
        if value_select is ValueSelect:
            x = [value_select(custom_values) for i in range(multiplier)]
        else:
            x = [value_select() for i in range(multiplier)]
        super(MultiValueSelect, self).__init__(x)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    @property
    def value(self):
        if isinstance(self[0], NumericValue):
            number = 0
            for i, value in enumerate(self[::-1]):
                number += int(value) * math.pow(self[0].base, i)
            return int(number)
        else:
            string = ""
            for value_select in self:
                string += value_select.value  # not calling str which ljust's
            return string


class ValueSelectString(list):
    """A list of ValueSelect's and characters, representing a string."""
    def __init__(self, format, custom_values=None):
        super(ValueSelectString, self).__init__()
        self.format = format
        self.values = list()  # lists of value selects representing a value

        multiplier = 1
        char_spec = False
        for character in self.format:
            if not char_spec:
                if character == "%":
                    char_spec = True
                    multiplier = 1
                else:
                    #multiplier = 1
                    self.append(character)
                continue

            # this is a character specifier
            if is_number(character):
                multiplier = int(character)
                continue

            try:
                value_select = VALUE_SELECTS[character]
            except KeyError:
                raise UnknownSpecifierError(
                    "'%s' is an unknown specifier." % character
                )
            else:
                if value_select is ReturnCharacter:
                    self.append(ReturnCharacter())
                else:
                    mvs = MultiValueSelect(
                        multiplier, value_select, custom_values
                    )
                    self.values.append(mvs)
                    self.extend(mvs)
            finally:
                char_spec = False

    def __str__(self):
        values = [str(char) for char in self]
        return "".join(values)

    @property
    def selected_values(self):
        """Returns a list of currently selected values."""
        return [v.value for v in self.values]

    def instanceindex(self, instance_type):
        """Returns the first index of an instance of `instance_type`"""
        for i, vs in enumerate(self):
            if isinstance(vs, instance_type):
                return i

        raise TypeError(
            "%s is not in %s (%s)" % (instance_type, type(self), self.format)
        )

    def value_at(self, string_index):
        """Returns the ValueSelect or character at the string index.
        The string index is the index of this ValueSelectString as if it is
        being treated as a string.

        Example::

            cs0 == CustomValueSelect == ["bb", "cc"]
            cs1 == CustomValueSelect == ["dd", "ee"]
            vss == ValueSelectString == ["a", cs0, cs1, "f"]
            vss == ["a", ["bb", "cc"], ["dd", "ee"], "f"]
            str(vss) == "abbddf"
            vss.value_at(0) == "a"
            vss.value_at(1) == cs0
            vss.value_at(2) == cs0
            vss.value_at(3) == cs1
            vss.value_at(5) == "f"
            str(vss.value_at(2)) == "bb"
        """
        # keep looping until we're at the index we want
        char_index = vs_index = 0
        while string_index > 0:
            string_index -= 1
            # if it's not a value select then go to the next index
            if not isinstance(self[vs_index], ValueSelect):
                char_index = 0
                vs_index += 1
                continue

            char_index += 1
            if char_index >= self[vs_index].longest_len:
                char_index = 0
                vs_index += 1

        # return state
        return self[vs_index]


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)


def is_number(character):
    """Returns True if given character is a number, False otherwise."""
    try:
        int(character)
        return True
    except ValueError:
        return False


def is_selectable_character(display_string, col):
    """Returns True if the character can be selected"""
    # keep looping until we're at the index we want
    char_index = vs_index = 0
    while col > 0:
        col -= 1

        char_index += 1
        if isinstance(display_string[vs_index], ValueSelect):
            width = display_string[vs_index].longest_len
        else:
            width = 1
        if char_index >= width:
            char_index = 0
            vs_index += 1

    # selectable if we're at the start of a value select or returnchar
    return char_index == 0 and (
        isinstance(display_string[vs_index], ValueSelect) or
        isinstance(display_string[vs_index], ReturnCharacter)
    )


# defined here because we need to build classes first
VALUE_SELECTS = {
    'c': CharacterValueSelect,
    'C': CapsCharacterValueSelect,
    'i': IntegerValueSelect,
    'd': IntegerValueSelect,
    'x': HexadecimalValueSelect,
    'X': HexadecimalValueSelect,
    '.': PunctuationValueSelect,
    'm': ValueSelect,
    'r': ReturnCharacter,
}
