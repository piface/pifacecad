########
Examples
########

.. note:: Remember to use ``python3``.

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
    >>> cad.switches[0].value  # reads the value of switch 0
    1
    >>> cad.switch_port.value


IR Receiver
===========

.. warning:: Similar to interrupts, this is subject to change (I'm not totally
   happy with this implementation - should be using threads and stuff).

.. todo:: link to example config

You first need to define which IR codes are available to your program in your
~/.lircrc::

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


Then you define a function you want to run, register it and then call
:func:`pifacecad.wait_for_ir`::

    >>> import pifacecad
    >>> pifacecad.init()

    >>> def print_ir_code(ir_code):
    ...     print(ir_code)
    ...     return True  # keep waiting
    ...
    >>> ifm = pifacecad.IRFunctionMap()
    >>> ifm.register(ir_code="one", callback=print_ir_code)

    >>> pifacecad.wait_for_ir(ir_func_map=ifm, prog="pifacecadexample")

Now when you press 1 on your remote, "one" is printed to the screen.

Interrupts
==========

A poor way of checking the inputs for activity is to periodically poll them. A
better way is to register tasks you would like to be completed when the input
event occurs.

.. warning:: Interrupts are subject to change (I'm not totally happy with this
   implementation - should be using threads and stuff).

We're going to use :class:`pifacecommon.interrupts.InputFunctionMap`::

    >>> import pifacecommon
    >>> import pifacecad

    >>> pifacecad.init()
    >>> cad = pifacecad.PiFaceCAD()

    >>> def write_hello(flag, state):
    ...     cad.lcd.write("Hello")
    ...     return True  # keep waiting for interrupts
    ...

    >>> # when switch 0 is pressed, run write_hello
    >>> ifm = pifacecommon.InputFunctionMap()
    >>> ifm.register(
            input_num=0,
            direction=pifacecommon.IN_EVENT_DIR_ON,
            callback=write_hello)

    >>> pifacecad.wait_for_input(ifm)
