# Copyright 2012, Oliver Nagy <olitheolix@gmail.com>
#
# This file is part of QBash.
#
# QBash is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# QBash is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with QBash. If not, see <http://www.gnu.org/licenses/>.

"""
This module contains only constants to convert colours or key-codes.
"""

from PyQt4 import QtCore, QtGui

# Define the colours returned by Pyte in terms of QColor objects.
colorCodesQt = {'black':   QtGui.QColor(0x00, 0x00, 0x00),
                'red':     QtGui.QColor(0xaa, 0x00, 0x00),
                'green':   QtGui.QColor(0x00, 0xaa, 0x00),
                'blue':    QtGui.QColor(0x00, 0x00, 0xaa),
                'cyan':    QtGui.QColor(0x00, 0xaa, 0xaa),
                'brown':   QtGui.QColor(0xaa, 0xaa, 0x00),
                'yellow':  QtGui.QColor(0xff, 0xff, 0x44),
                'magenta': QtGui.QColor(0xaa, 0x00, 0xaa),
                'white':   QtGui.QColor(0xff, 0xff, 0xff)}


def strToQColorForeground(colorFg, colorBg):
    # Look up the foreground colour, or resort to white if it is unknown.
    if colorFg in colorCodesQt:
        fg = colorCodesQt[colorFg]
    else:
        fg = colorCodesQt['white']

    # Look up the foreground colour, or resort to black if it is unknown.
    if colorBg in colorCodesQt:
        bg = colorCodesQt[colorBg]
    else:
        bg = colorCodesQt['black']

    # Return the QColor tuple.
    return (fg, bg)


def QtKeyToAscii(event):
    """
    (Try to) convert the Qt key event to the corresponding ASCII sequence for
    the terminal. This works fine for standard alphanumerical characters, but
    most other characters require terminal specific control sequences.

    The conversion below works for TERM="linux' terminals.
    """
    if event.modifiers() == QtCore.Qt.ControlModifier:
        if event.key() == QtCore.Qt.Key_P:
            return b'\x10'
        elif event.key() == QtCore.Qt.Key_N:
            return b'\x0E'
        elif event.key() == QtCore.Qt.Key_C:
            return b'\x03'
        elif event.key() == QtCore.Qt.Key_B:
            return b'\x02'
        elif event.key() == QtCore.Qt.Key_F:
            return b'\x06'
        elif event.key() == QtCore.Qt.Key_D:
            return b'\x04'
        elif event.key() == QtCore.Qt.Key_O:
            return b'\x0F'
        else:
            return None
    else:
        if event.key() == QtCore.Qt.Key_Return:
            return '\n'.encode('utf-8')
        elif event.key() == QtCore.Qt.Key_Enter:
            return '\n'.encode('utf-8')
        elif event.key() == QtCore.Qt.Key_Tab:
            return '\t'.encode('utf-8')
        elif event.key() == QtCore.Qt.Key_Backspace:
            return b'\x08'
        elif event.key() == QtCore.Qt.Key_Enter:
            return '\n'.encode('utf-8')
        elif event.key() == QtCore.Qt.Key_Home:
            return b'\x47'
        elif event.key() == QtCore.Qt.Key_End:
            return b'\x4f'
        elif event.key() == QtCore.Qt.Key_Left:
            return b'\x02'
        elif event.key() == QtCore.Qt.Key_Up:
            return b'\x10'
        elif event.key() == QtCore.Qt.Key_Right:
            return b'\x06'
        elif event.key() == QtCore.Qt.Key_Down:
            return b'\x0E'
        elif event.key() == QtCore.Qt.Key_PageUp:
            return b'\x49'
        elif event.key() == QtCore.Qt.Key_PageDown:
            return b'\x51'
        elif event.key() == QtCore.Qt.Key_F1:
            return b'\x1b\x31'
        elif event.key() == QtCore.Qt.Key_F2:
            return b'\x1b\x32'
        elif event.key() == QtCore.Qt.Key_F3:
            return b'\x1b\x33'
        elif event.key() == QtCore.Qt.Key_F4:
            return b'\x1b\x34'
        elif event.key() == QtCore.Qt.Key_F5:
            return b'\x1b\x35'
        elif event.key() == QtCore.Qt.Key_F6:
            return b'\x1b\x36'
        elif event.key() == QtCore.Qt.Key_F7:
            return b'\x1b\x37'
        elif event.key() == QtCore.Qt.Key_F8:
            return b'\x1b\x38'
        elif event.key() == QtCore.Qt.Key_F9:
            return b'\x1b\x39'
        elif event.key() == QtCore.Qt.Key_F10:
            return b'\x1b\x30'
        elif event.key() == QtCore.Qt.Key_F11:
            return b'\x45'
        elif event.key() == QtCore.Qt.Key_F12:
            return b'\x46'
        elif event.text() in ('abcdefghijklmnopqrstuvwxyz'
                              'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                              '[],=-.;/`&^~*@|#(){}$><%+?"_!'
                              "'\\"):
            return event.text().encode('utf8')
        else:
            return None
