======
QBash
======

QBash embeds a Bash shell inside a Qt widget.

The terminal emulation is provided by `Pyte
<https://github.com/selectel/pyte>`_.

The `bin/demo.py` script features an example of how to embed QBash
into Qt programs.

Installation
============

QBash depends on `Pyte`, `PyQt4` and `Python 3.x`.

On Debian based systems like (K)Ubuntu, the necessary dependencies
can be installed with

.. code-block:: bash

   sudo apt-get install git python3-pyqt4 python3-pip
   sudo pip3 install pyte

Demo and Screenshots
====================
Use the following commands to run the demo:

.. code-block:: bash

   git clone https://github.com/qtmacsdev/qbash.git
   cd qbash/bin
   python3 demo.py

.. image:: screenshots/qbash_ls.png
.. image:: screenshots/qbash_top.png
.. image:: screenshots/qbash_mc.png

LICENSE
=======

QBash is licensed under the terms of the GPL.
