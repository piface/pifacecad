############
Installation
############

Make sure you are using the lastest version of Raspbian::

    $ sudo apt-get update
    $ sudo apt-get upgrade

Install ``pifacecad`` (for Python 3 and 2) with the following command::

    $ sudo apt-get install python{,3}-pifacecad

Test by running the ``sysinfo.py`` program::

    $ python3 /usr/share/doc/python3-pifacecad/examples/sysinfo.py

You will need to `configure the IR receiver <lirc.html#setting-up-the-infrared-receiver>`_ yourself. More examples can be found in `/usr/share/doc/python3-pifacecad/examples/` (which may need unzipping using `gunzip`).

SysInfo Service
===============

You can run `sysinfo` as a service using::

    $ sudo service pifacecadsysinfo start

You can stop the service with::

    $ sudo service pifacecadsysinfo stop

You can enable the service to run at boot (handy for headless Raspberry Pi's)::

    $ sudo update-rc.d pifacecadsysinfo defaults
