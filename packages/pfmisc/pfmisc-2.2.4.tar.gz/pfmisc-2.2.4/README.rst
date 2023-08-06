################
pfmisc  v2.2.4
################

.. image:: https://badge.fury.io/py/pfmisc.svg
    :target: https://badge.fury.io/py/pfmisc

.. image:: https://travis-ci.org/FNNDSC/pfdcm.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pfmisc

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pfmisc

.. contents:: Table of Contents

********
Overview
********

This repository provides ``pfmisc`` -- miscellaneous services for the ``pf`` family.

Most simply, ``pfmisc`` provides debug, text-console colorization, and error modules.

*****
Usage
*****

Simply do a

.. code-block:: python

    import pfmisc

    class MyClass():

        def __init__(self, *args, **kwargs):
            self.debug  = pfmisc.debug()

            self.debug.qprint('hello there!')

which will result in some decent debugging in stdout.

************
Installation
************

Installation is relatively straightforward, and best done with ``pip``:

.. code-block:: bash

    pip install pfmisc

*****
Notes
*****

Please examine the ``pfmisc.py`` code for hints on how to use/call the various debugging and error modules:

.. code-block:: html

    https://github.com/FNNDSC/pfmisc



