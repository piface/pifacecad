import sys
from distutils.core import setup


#PY3 = sys.version_info.major >= 3
PY3 = sys.version_info[0] >= 3
VERSION_FILE = "pifacecad/version.py"


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


setup(
    name='pifacecad',
    version=get_version(),
    description='The PiFace Control And Display module.',
    author='Thomas Preston',
    author_email='thomas.preston@openlx.org.uk',
    license='GPLv3+',
    url='http://piface.github.io/pifacecad/',
    packages=['pifacecad', 'pifacecad.tools'],
    long_description=open('README.md').read() + open('CHANGELOG').read(),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or "
        "later (AGPLv3+)",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='piface cad control display raspberrypi openlx',
    requires=['pifacecommon', 'lirc'],
)
