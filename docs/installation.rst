############
Installation
############

First, you will need to install ``lirc``::

    $ sudo apt-get install lirc

Then you will need to download and install the latest releases of
(using ``sudo dpkg -i``):

- `pifacecommon <https://github.com/piface/pifacecommon/releases>`_
- `python-lirc <https://github.com/tompreston/python-lirc/releases>`_
  Python 3 support for LIRC. Be sure to install the correct architecture
  (**armhf** for a Raspberry Pi).

Then download the latest PiFace CAD Debian package from
`here <https://github.com/piface/pifacecad/releases>`_ and install with:

.. parsed-literal::

    $ sudo dpkg -i python3-pifacecad\_\ |version|-1_all.deb

.. note:: Python 2 users will want to use python-pifacecad\_\ |version|-1_all.deb.

Test by running the ``sysinfo.py`` program::

    $ python3 /usr/share/doc/python3-pifacecad/examples/sysinfo.py

You will need to `configure the IR receiver <lirc.html#setting-up-the-infrared-receiver>`_ yourself.

SysInfo Service
===============

You can run `sysinfo` as a service using::

    $ sudo service pifacecadsysinfo start

You can stop the service with::

    $ sudo service pifacecadsysinfo stop

You can enable the service to run at boot (handy for headless Raspberry Pi's)::

    $ sudo update-rc.d pifacecadsysinfo enable
