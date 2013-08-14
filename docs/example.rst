########
Examples
########

Basic usage
===========

Set up::

    >>> import pifacecad
    >>> pifacecad.init()  # initialises PiFace Control and Display

Playing with PiFace Control and Display::

    >>> cad = pifacecad.PiFaceCAD()    # create PiFace Control and Display object
    >>> cad.lcd.backlight_on()         # turns the backlight on
    >>> cad.lcd.write("Hello, world!") # writes hello world on to the LCD
    >>>
    >>> cad.switches[3].value  # reads the value of switch 3
    1
    >>> cad.switch_port.value  # reads the value of the switch port
    4


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
    >>> pifacecad.init()

    >>> def print_ir_code(event):
    ...     print(event.ir_code)
    ...
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
    >>> pifacecad.init()
    >>> cad = pifacecad.PiFaceCAD()
    >>> cad.lcd.write("You pressed: ")
    >>> def update_pin_text(event):
    ...     cad.lcd.set_cursor(13, 0)
    ...     cad.lcd.write(str(event.pin_num))
    ...
    >>> listener = pifacecad.SwitchEventListener()
    >>> for i in range(8):
    ...     listener.register(i, pifacecad.IODIR_ON, update_pin_text)
    >>> listener.activate()

The screen should update as buttons are pressed. To stop the listener, call
it's ``deactivate`` method:

    >>> listener.deactivate()

The :class:`Event` object has some interesting attributes. You can access them
like so::

    >>> import pifacecad
    >>> pifacecad.init()
    >>> def print_event_info(event):
    ...     print("Flag:     ", bin(event.interrupt_flag))
    ...     print("Capture:  ", bin(event.interrupt_capture))
    ...     print("Pin num:  ", event.pin_num)
    ...     print("Direction:", event.direction)
    ...
    >>> listener = pifacecad.SwitchEventListener()
    >>> listener.register(0, pifacecad.IODIR_OFF, print_event_info)
    >>> listener.activate()

This would print out the event informaion whenever you unpress switch 0::

    Flag:      0b00000001
    Capture:   0b11111110
    Pin num:   0
    Direction: 1
