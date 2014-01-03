#######################
Creating Custom Bitmaps
#######################

You can store up to eight custom bitmaps using PiFace Control and Display. Each
bitmap describes a single character on the LCD screen (5x8 pixels).

To create a custom bitmap you instantiate an :class:`LCDBitmap` which takes a list
of binary values each describing a line. For example::

    >>> quaver = pifacecad.LCDBitmap([0, 2, 3, 2, 14, 30, 12, 0])

or as hex::

    >>> quaver = pifacecad.LCDBitmap([0x0, 0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0])

or as binary (you can almost see the bitmap image here)::

    >>> quaver = pifacecad.LCDBitmap([0b00000,
    ...                               0b00010,
    ...                               0b00011,
    ...                               0b00010,
    ...                               0b01110,
    ...                               0b11110,
    ...                               0b01100,
    ...                               0b00000])

.. note:: You can use `this tool <http://www.quinapalus.com/hd44780udg.html>`_
   to help design custom bitmaps. Make sure you select 5x8.

You store and display custom bitmaps with the following commands::

    >>> cad = pifacecad.PiFaceCAD()
    >>> cad.lcd.store_custom_bitmap(0, quaver)
    >>> cad.lcd.write_custom_bitmap(0)

Here is a complete code example::

    >>> import pifacecad
    >>> cad = pifacecad.PiFaceCAD()
    >>> quaver = pifacecad.LCDBitmap([0x0, 0x2, 0x3, 0x2, 0xe, 0x1e, 0xc, 0x0])
    >>> cad.lcd.store_custom_bitmap(0, quaver)
    >>> cad.lcd.write_custom_bitmap(0)
