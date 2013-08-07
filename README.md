pifacecad
=========

PiFace Control and Display Python module.

Contrast is adjusted with screwdriver + screw by IR node.


Documentation
=============

[http://piface.github.io/pifacecad/](http://piface.github.io/pifacecad/)


Install
=======

Download the latest debian package from
[here](https://github.com/piface/pifacecad/releases) and install with:

    $ dpkg -i python3-pifacecad_1.0.0-1_all.deb

You may need to download and install the latest releases of:

- [pifacecommon](https://github.com/piface/pifacecommon/releases)
- [python-lirc](https://github.com/tompreston/python-lirc/releases)
  (Python 3 support for LIRC)

You might also need to reboot.

Or you can install without using your package manager:

    $ git clone https://github.com/piface/pifacecad.git
    $ cd pifacecad/
    $ sudo python3 setup.py install
    $ bin/post-installation.sh

*Replace `python3` for `python` if you're using Python 2.*
