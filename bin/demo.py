#!/usr/bin/python3

import os
import sys
import argparse
from PyQt4 import QtGui

# Terminal size.
numLines = 24
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
QtApplicationInstance = QtGui.QApplication(sys.argv)
mainWidget = qbash.QBash(numLines=numLines, numColumns=numColumns)
mainWidget.show()
sys.exit(QtApplicationInstance.exec_())
