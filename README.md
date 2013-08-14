pifacecad
=========

PiFace Control and Display Python module.

Contrast is adjusted with screwdriver + screw by IR node.


Documentation
=============

[http://piface.github.io/pifacecad/](http://piface.github.io/pifacecad/)

You can also find the documentation and some examples installed at:

    /usr/share/doc/python3-pifacecad/

Install
=======

Download the latest debian package from
[here](https://github.com/piface/pifacecad/releases) and install with:

    $ dpkg -i python3-pifacecad_1.0.0-1_all.deb

You may need to download and install the latest releases of:

- [pifacecommon](https://github.com/piface/pifacecommon/releases)
- [python-lirc](https://github.com/tompreston/python-lirc/releases)
  (Python 3 support for LIRC)

You will also need to [configure the IR Receiver](http://piface.github.io/pifacecad/lirc.html#setting-up-the-infrared-receiver) and reboot.

Test by running the ``sysinfo.py`` program:

    python3 /usr/share/doc/python3-pifacecad/examples/sysinfo.py
