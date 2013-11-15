Tools
=====

There are some tools provided with PiFace Control and Display which simplify
getting input from a user.

Question
--------
:class:`pifacecad.tools.question.LCDQuestion` will display a question on the
top row and an answer on the  bottom. The user can cycle through answers by
moving the navigation switch left and right and select an answer by pressing
the navigation switch in.

It can be used like this::

    >>> import pifacecad
    >>> from pifacecad.tools.question import LCDQuestion

    >>> question = LCDQuestion(question="What is 5 x 2?", answers=["1", "10", "12"])
    >>> answer_index = question.ask()

You can pass in an already initialised Control and Display object and also
specify a custom selector::

    >>> import pifacecad
    >>> from pifacecad.tools.question import LCDQuestion

    >>> customcad = pifacecad.PiFaceCAD()
    >>> customcad.lcd.cursor_off()
    >>> customcad.lcd.blink_off()

    >>> question = LCDQuestion(question="What is 5 x 2?",
    ...                        answers=["1", "10", "12"],
    ...                        selector="#",
    ...                        cad=customcad)
    >>> answer_index = question.ask()

Scanf
-----
:class:`pifacecad.tools.scanf.LCDScanf` will display a custom string that
can be modified using the navigation switch. In 'select' mode, moving the
navigation switch left or right (switches 6 and 7) selects a character.
Change to 'edit' mode by pressing the navigation switch in (switch 5).
In edit mode, moving the navigation switch left or right changes the character.

To return the input, move the cursor under the 'enter' arrow and press the
navigation switch in.

The `LCDScanf` class can be used like this::

    >>> import pifacecad
    >>> from pifacecad.tools.scanf import LCDScanf

    >>> scanner = LCDScanf("Text: %c%2i%.%r")
    >>> print(scanner.scan())  # user enters things on PiFace C&D
    ['a', '13', '!']

The format string defines editable variables using a `%` symbol. The
format specification is::

    c: Characters
    C: Capital Characters
    i: Integers
    d: Integers
    x: Hexadecimal
    X: Capital Hexadecimal
    .: Punctuation
    m: Custom (specifed by ``custom_values`` in init args)
    r: Return (switch 5 to submit string)

To add multiple characters in the same variable you can specify a number
after the `%` symbol. For example, to request that the user enter a two
digit integer::

    >>> print(LCDScanf("%2i%r").scan())
    ['42']

You can use the `m` specifier to enter custom variable values::

    >>> scanner = LCDScanf("Animal: %m%r", custom_values=('cat', 'dog', 'fish'))
    >>> print(scanner.scan())
    ['fish']
