pifacecad
===============

The PiFace Human Interface module.

Contrast is adjusted with screwdriver + screw by IR node.

Dependencies
============
(handled by the install script)
[python-lirc](https://github.com/tompreston/python-lirc) LIRC support for
Python 3
[pifacecommon](https://github.com/piface/pifacecommon)

Installation
============

    $ sudo ./install.sh


Examples
=======
### Basic usage

    >>> import pifacecad
    >>> pifacecad.init()  # initialises the PiFace Human Interface
    >>>
    >>> pfcad = pifacecad.PiFaceCAD() # create PiFace Control and Display object
    >>> pfcad.lcd.backlight_on()         # turns the backlight on
    >>> pfcad.lcd.write("Hello, world!") # writes hello world on to the LCD
    >>> 
    >>> pifacecad.switches[0].value  # reads the value of switch 0
    1
    >>> pifacecad.switch_port.value

### Interrupts
Similar to [PiFace Digital Interrupts](https://github.com/piface/pifacedigitalio#interrupts).

### IR Interrupts
    >>> import pifacecad
    >>> pifacecad.init()
    >>> pfcad = pifacecad.PiFaceCAD()
    >>> 
    >>> def turn_backlight_on(ircode):
    ... pfcad.lcd.backlight_on()
    ... return True
    ... 
    >>> def turn_backlight_off(ircode):
    ... pfcad.lcd.backlight_off()
    ... return True
    ...
    >>> def write_message_and_exit(ircode):
    ... pfcad.lcd.write("Hello, World!")
    ... return False
    ...
    >>> irfm = pifacecad.IRFunctionMap()
    >>> irfm.register(ir_code="one", callback=turn_backlight_on)
    >>> irfm.register(ir_code="two", callback=turn_backlight_off)
    >>> irfm.register(ir_code="three", callback=write_message_and_exit)
    >>> 
    >>> pifacecad.wait_for_ir(
    ...     ir_func_map=irfm, 
    ...     ir_config="./lircconf",
    ...     prog="pifacecadtest"
    ... )
