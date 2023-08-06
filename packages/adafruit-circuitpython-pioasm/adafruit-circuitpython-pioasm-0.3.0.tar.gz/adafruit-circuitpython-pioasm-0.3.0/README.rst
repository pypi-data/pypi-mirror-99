Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-pioasm/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/pioasm/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_PIOASM/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_PIOASM/actions
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

Simple assembler to convert pioasm to bytes


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-pioasm/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-pioasm

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-pioasm

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-pioasm

Usage Example
=============

.. code-block:: python

    import time
    import rp2pio
    import board
    import adafruit_pioasm

    squarewave = """
    .program squarewave
        set pins 1 [1]  ; Drive pin high and then delay for one cycle
        set pins 0      ; Drive pin low
    """

    assembled = adafruit_pioasm.assemble(squarewave)

    sm = rp2pio.StateMachine(
        assembled,
        frequency=80,
        init=adafruit_pioasm.assemble("set pindirs 1"),
        first_set_pin=board.LED,
    )
    print("real frequency", sm.frequency)

    time.sleep(120)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_PIOASM/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
