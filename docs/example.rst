########
Examples
########

Basic usage
===========

Hello, World!::

    >>> import pifacecad

    >>> cad = pifacecad.PiFaceCAD()    # create PiFace Control and Display object
    >>> cad.lcd.backlight_on()         # turns the backlight on
    >>> cad.lcd.write("Hello, world!") # writes hello world on to the LCD

Reading the switches::

    >>> cad.switches[3].value  # reads the value of switch 3
    1
    >>> cad.switch_port.value  # reads the value of the switch port
    4

Cursor control::

    >>> cad.lcd.set_cursor(4, 1)  # set the cursor to col 4 on the second row
    >>> cad.lcd.cursor_off()      # turns the cursor off
    >>> cad.lcd.write("3.141592") # writes π to the LCD

    >>> cad.lcd.blink_off()       # turns the blinking off
    >>> cad.lcd.cursor_on()       # turns the cursor on
    >>> cad.lcd.home()            # send the cursor home

    >>> cad.lcd.write("PiFace Control\nand Display")  # '\n' starts a new line
    >>> cad.lcd.clear()           # clear the screen (also sends the cursor home)

The LCD has more RAM than just the 16x2 characters that you can see::

    >>> cad.lcd.write("Something really, really long.")
    >>> cad.lcd.move_right()
    >>> cad.lcd.move_left()
    >>> cad.lcd.see_cursor()  # move the display so that we can see the cursor

The `viewport_corner` variable describes which column the top left display
character is showing from RAM::

    >>> cad.lcd.viewport_corner       # inspect the viewport_corner variable
    8
    >>> cad.lcd.viewport_corner = 15  # set the viewport_corner variable

You can also `create your own custom bitmaps <creating_custom_bitmaps.html>`_.

IR Receiver
===========

You need to add your LIRC client (your program) to ~/.lircrc::

    $ cat ~/.lircrc
    begin
      prog = pifacecadexample
      button = 1
      config = one
    end

    begin
      prog = pifacecadexample
      button = 2
      config = two
    end

Then, register IR codes to functions using :class:`IREventListener`::

    >>> import pifacecad

    >>> def print_ir_code(event):
    ...     print(event.ir_code)
    ...
    >>> pifacecad.PiFaceCAD()  # initialise a PiFace Control and Display board
    >>> listener = pifacecad.IREventListener(prog="pifacecadexample")
    >>> listener.register('one', print_ir_code)
    >>> listener.register('two', print_ir_code)
    >>> listener.activate()

Now when you press 1 or 2 on your remote, "one" or "two" is printed.

Interrupts
==========

Instead of polling the switches we can use the :class:`SwitchEventListener` to
register actions that we wish to be called on certain switch events.

    >>> import pifacecad
    >>> def update_pin_text(event):
    ...     event.chip.lcd.set_cursor(13, 0)
    ...     event.chip.lcd.write(str(event.pin_num))
    ...
    >>> cad = pifacecad.PiFaceCAD()
    >>> cad.lcd.write("You pressed: ")
    >>> listener = pifacecad.SwitchEventListener(chip=cad)
    >>> for i in range(8):
    ...     listener.register(i, pifacecad.IODIR_FALLING_EDGE, update_pin_text)
    >>> listener.activate()

The screen should update as buttons are pressed. To stop the listener, call
it's ``deactivate`` method:

    >>> listener.deactivate()


The :class:`Event` object has some interesting attributes. You can access them
like so::

    >>> import pifacecad
    >>> cad = pifacecad.PiFaceCAD()
    >>> listener = pifacecad.SwitchEventListener(chip=cad)
    >>> listener.register(0, pifacecad.IODIR_RISING_EDGE, print)
    >>> listener.activate()

This would print out the event informaion whenever you unpress switch 0::

    interrupt_flag:    0b1
    interrupt_capture: 0b11111111
    pin_num:           0
    direction:         1
    chip:              <pifacecad.core.PiFaceCAD object at 0xb682dab0>
    timestamp:         1380893579.447889
