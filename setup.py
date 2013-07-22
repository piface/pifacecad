import os
import sys
import stat
import errno
import shutil
import subprocess
from distutils.core import setup


PY3 = sys.version_info.major >= 3
PYTHON_CMD = "python3" if PY3 else "python"
VERSION_FILE = "pifacecad/version.py"

# change this to True if you just want to install the module by itself
MODULE_ONLY = False

INSTALL_PIFACECOMMON_CMD = \
    "git clone https://github.com/piface/pifacecommon.git && " \
    "cd pifacecommon && " \
    "{} setup.py install".format(PYTHON_CMD)

INSTALL_PYTHON_LIRC_CMD = \
    "git clone https://github.com/tompreston/python-lirc.git &&" \
    "cd python-lirc && " \
    "{} setup.py install".format(PYTHON_CMD)

INSTALL_LIRC_CMD = "apt-get install lirc"

KEY_MAP_INSTRUCTIONS = "https://piface.github.io/pifacecad/lirc/#keymap"


class InstallFailed(Exception):
    pass


def get_version():
    if PY3:
        version_vars = {}
        with open(VERSION_FILE) as f:
            code = compile(f.read(), VERSION_FILE, 'exec')
            exec(code, None, version_vars)
        return version_vars['__version__']
    else:
        execfile(VERSION_FILE)
        return __version__


def run_cmd(cmd, error_msg):
    success = subprocess.call([cmd], shell=True)
    if success != 0:
        raise InstallFailed(error_msg)


def install_pifacecommon():
    print("Installing pifacecommon.")
    run_cmd(INSTALL_PIFACECOMMON_CMD, "Failed to install pifacecommon.")


def install_python_lirc():
    print("Installing pifacecommon.")
    run_cmd(INSTALL_PYTHON_LIRC_CMD, "Failed to install python-lirc.")


def check_pifacecommon():
    try:
        import pifacecommon
        # TODO version numbers
    except ImportError:
        print("pifacecommon is not installed.")
        install_pifacecommon()


def check_python_lirc():
    try:
        import lirc
        # TODO version numbers
    except ImportError:
        print("lirc is not installed.")
        install_python_lirc()


def setup_lirc():
    # install lirc
    run_cmd(INSTALL_LIRC_CMD, "Failed to install lirc.")

    # setup /etc/modules
    # check if lines are already there
    write_lirc_dev = write_lirc_rpi = True
    with open('/etc/modules', 'r') as modfile:
        for line in modfile:
            if "lirc_dev" in line:
                write_lirc_dev = False
            if "lirc_rpi gpio_in_pin=23" in line:
                write_lirc_rpi = False
    # write them
    if write_lirc_dev or write_lirc_rpi:
        with open('/etc/modules', 'a') as modfile:
            if write_lirc_dev:
                modfile.write("lirc_dev\n")
            if write_lirc_rpi:
                modfile.write("lirc_rpi gpio_in_pin=23\n")

    # setup /etc/lirc/hardware.conf
    shutil.copyfile(
        "/etc/lirc/hardware.conf", "/etc/lirc/hardware.conf.backup")
    # TODO make this grab the file from the web
    shutil.copyfile("bin/lirc_hardware.conf", "/etc/lirc/hardware.conf")
    os.chmod(
        "/etc/lirc/hardware.conf",
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IXGRP |
        stat.S_IROTH | stat.S_IXOTH)

    # point to documentation
    print(
        "\n\n\tYou will need to generate a key map for your remote.\n"
        "\tSee: {}\n\n".format(KEY_MAP_INSTRUCTIONS))


def install_service():
    # copy pifacecad sysinfo service files
    # TODO make this grab the file from the web
    #sysinfo_httpsrc = "examples/sysinfo.py"
    #sysinfodest = "/usr/local/bin/pifacecadsysinfo.py"
    #urllib.request.urlretrieve(sysinfo_httpsrc, sysinfodest)
    sysinfo_src = "examples/sysinfo.py"
    sysinfo_dest = "/usr/local/bin/pifacecadsysinfo.py"
    shutil.copyfile(sysinfo_src, sysinfo_dest)

    sysinfo_service_src = "bin/pifacecadsysinfo.sh"
    sysinfo_service_dest = "/etc/init.d/pifacecadsysinfo"
    shutil.copyfile(sysinfo_service_src, sysinfo_service_dest)
    os.chmod(
        sysinfo_service_dest,
        stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR |
        stat.S_IRGRP | stat.S_IXGRP |
        stat.S_IROTH | stat.S_IXOTH)


# don't do setup(), just install service
if "install_service" in sys.argv:
    install_service()
    sys.exit()


if "install" in sys.argv and not MODULE_ONLY:
    check_pifacecommon()
    check_python_lirc()
    setup_lirc()


setup(
    name='pifacecad',
    version=get_version(),
    description='The PiFace Control And Display module.',
    author='Thomas Preston',
    author_email='thomasmarkpreston@gmail.com',
    license='GPLv3+',
    url='http://pi.cs.man.ac.uk/interface.htm',
    packages=['pifacecad', 'pifacecad.tools'],
    long_description="pifacecad provides I/O functions and classes for the "
        "PiFace CAD Raspberry Pi extension",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='piface cad raspberrypi openlx',
    requires=['pifacecommon'],
)
