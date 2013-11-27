Included Examples
=================
The PiFace Control and Display Python libraries include some example programs
at ``/usr/share/doc/python3-pifacecad/examples/``. You are encouraged to
modify and improve them.

You can also find the examples on `GitHub <https://github.com/piface/pifacecad/tree/master/examples>`_.

.. note:: Some of the included examples are zipped (`.gz`) and require
         unzipping before they can be used.

Internet Radio
--------------
An internet radio with IR remote control features.

.. note:: In order to use the infrared remote control features of the radio
          you must first `configure LIRC <lirc.html>`_ and configure the
          buttons  in ``/usr/share/doc/python3-pifacecad/examples/radiolircrc``
          so that they match the buttons on your remote (in
          ``/etc/lirc/lircd.conf``).

The internet radio requires the program ``mplayer`` to be installed in order to
play audio streams. Install it with::

    $ sudo apt-get install mplayer

Unzip the radio::

    $ gunzip /usr/share/doc/python3-pifacecad/examples/radio.py.gz

Run the radio::

    $ python3 /usr/share/doc/python3-pifacecad/examples/radio.py

================ ==================
Button           Function
================ ==================
Navigation left  Previous station
Navigation right Next station
Navigation in    Stop/Start playing
Control 0        Station Preset 0
Control 1        Station Preset 1
Control 2        Station Preset 2
Control 3        Station Preset 3
Control 4        Exit
================ ==================

Hangman
-------
A game of hangman. Guess which letters are in the word. To many incorrect
guesses and, well, you know the rest.

Unzip and run hangman::

    $ gunzip /usr/share/doc/python3-pifacecad/examples/radio.py.gz
    $ python3 /usr/share/doc/python3-pifacecad/examples/radio.py

================ =========================
Button           Function
================ =========================
Navigation left  Move cursor/Change letter
Navigation right Move cursor/Change letter
Navigation in    Change mode/enter
================ =========================

See hangman in action on `YouTube <http://youtu.be/XAM5vru8ffY>`_.

Traintimes
----------
Shows UK train times from Manchester Picadilly (MAN) to various other stations.
Have a peek at the code to the alter which station you are departing from.

``traintimes.py`` depends on `Beautiful Soup 4 <http://www.crummy.com/software/BeautifulSoup/>`_. Install it with::

    $ sudo apt-get install python3-bs4

Then unzip and run traintimes::

    $ gunzip /usr/share/doc/python3-pifacecad/examples/traintimes.py.gz
    $ python3 /usr/share/doc/python3-pifacecad/examples/traintimes.py

================ ============================
Button           Function
================ ============================
Navigation left  Previous destination station
Navigation right Next destination station
Navigation in    Refresh
Control 4        Exit
================ ============================

Tweets
------
Shows latest tweets.

Twitter requires the `Python Twitter Tools <http://mike.verdone.ca/twitter/>`_
module to be installed::

    $ sudo apt-get install easy_install3
    $ sudo easy_install3 twitter

Unzip and run tweets::

    $ gunzip /usr/share/doc/python3-pifacecad/examples/tweets.py.gz
    $ python3 /usr/share/doc/python3-pifacecad/examples/tweets.py

================ ==============
Button           Function
================ ==============
Navigation left  Previous tweet
Navigation right Next tweet
Navigation in    Refresh
Control 4        Exit
================ ==============

Weather
-------
Shows current weather information. Unzip and run weather::

    $ gunzip /usr/share/doc/python3-pifacecad/examples/weather.py.gz
    $ python3 /usr/share/doc/python3-pifacecad/examples/weather.py

================ =================
Button           Function
================ =================
Navigation left  Previous location
Navigation right Next location
Navigation in    Refresh
Control 4        Exit
================ =================
