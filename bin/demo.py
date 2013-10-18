#!/usr/bin/python3

import os
import sys
import argparse
from PyQt4 import QtGui

# Terminal size in characters.
numLines = 25
numColumns = 80

# ----------------------------------------------------------------------
# Setup path to find QBash in the source directory.
# ----------------------------------------------------------------------
qbash_path = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, qbash_path)
import qbash.qbash as qbash

# ----------------------------------------------------------------------
# Setup the Qt application and start QBash.
# ----------------------------------------------------------------------

# Create the Qt application and QBash instance.
QtApplicationInstance = QtGui.QApplication(sys.argv)
widget = qbash.QBash(numLines=numLines, numColumns=numColumns)

# Resize QBash widget to (approximately) show the screen.
fmt = QtGui.QFontMetrics(widget.font())
width = fmt.width('8') * numColumns
height = fmt.height() * numLines
widget.resize(width + 5, height + 20)

# Show widget and launch Qt's event loop.
widget.show()
sys.exit(QtApplicationInstance.exec_())
