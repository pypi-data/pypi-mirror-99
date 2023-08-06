import sys
from distutils.core import setup

message = 'You tried to install "stan". The package for PyStan is named "pystan".'

argv = lambda x: x in sys.argv

if argv("install") or (argv("--dist-dir") and argv("bdist_egg")):  # pip install ..  # easy_install
    raise Exception(message)


if argv("bdist_wheel"):  # modern pip install
    raise Exception(message)


setup(
    name="stan",
    version="1.0",
    maintainer="Allen Riddell",
    maintainer_email="riddella@indiana.edu",
    long_description=message,
)
