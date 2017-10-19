pifacecad
=========

PiFace Control and Display Python module.

Contrast is adjusted with screwdriver + screw by IR node.


Documentation
=============

[http://pifacecad.readthedocs.org/](http://pifacecad.readthedocs.org/)

You can also find the documentation and some examples installed at:

    /usr/share/doc/python3-pifacecad/

Install
=======

Make sure you are using the latest version of Raspbian:

    $ sudo apt-get update
    $ sudo apt-get upgrade

Install `pifacecad` (for Python 3 and 2) with the following command:

    $ sudo apt-get install python{,3}-pifacecad

Test by running the `sysinfo.py` program:

    $ python3 /usr/share/doc/python3-pifacecad/examples/sysinfo.py

You will need to [configure the IR receiver](http://pifacecad.readthedocs.org/en/latest/lirc.html).

Install on Raspbian Strech and RaspberryPi 3
============================================

The piface packages are currently not in the main repositories. You can,
however, simply build them from their sources:

* Enable the spi-interface:

```
	$ sudo raspi-config
	Interfacing Options -> SPI -> Yes
```
* https://github.com/tompreston/python-lirc
```
	$ sudo aptitude install liblircclient-dev cython gcc python{,3}-setuptools python{,3}-dev
	$ git clone https://github.com/tompreston/python-lirc.git
	$ cd python-lirc/
	$ make py3 && sudo python3 setup.py install
	$ make py2 && sudo python setup.py install
```
* https://github.com/piface/pifacecommon
```
	$ git clone https://github.com/piface/pifacecommon.git
	$ cd pifacecommon/
	$ sudo python setup.py install
	$ sudo python3 setup.py install
```
* https://github.com/piface/pifacecad
```
	$ git clone https://github.com/piface/pifacecad.git
	$ cd pifacecad/
	$ sudo python setup.py install
	$ sudo python3 setup.py install
```
* run the hello world demo:
```
	>>> import pifacecad

	>>> cad = pifacecad.PiFaceCAD()    # create PiFace Control and Display object
	>>> cad.lcd.backlight_on()         # turns the backlight on
	>>> cad.lcd.write("Hello, world!") # writes hello world on to the LCD
```
* Cleanup: 
```
	$ sudo rm -rf pifacecad/ pifacecommon/ python-lirc/
```
