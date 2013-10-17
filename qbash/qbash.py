# Copyright 2012, Oliver Nagy <qtmacsdev@gmail.com>
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
QBash is a Qt widget that runs a Bash shell. The widget can be used and
embedded like any other Qt widget.

QBash is powered by Pyte, a Python based terminal emulator
(https://github.com/selectel/pyte).
"""
import os
import sys
import pty
import pyte
import qbash.util
from PyQt4 import QtCore, QtGui


class PollTerminal(QtCore.QObject):
    """
    Poll Bash.

    This class will run as a thread (started in ``QBash``) and poll the
    file descriptor of the Bash terminal.
    """
    # Signals to communicate with ``QBash``.
    startWork = QtCore.pyqtSignal()
    dataReady = QtCore.pyqtSignal(object)

    def __init__(self, fd, numLines, numColumns):
        super().__init__()

        # File descriptor that connects to Bash process.
        self.fd = fd

        # Setup Pyte (hard coded display size for now).
        self.screen = pyte.Screen(numColumns, numLines)
        self.stream = pyte.ByteStream()
        self.stream.attach(self.screen)

        # This slot will trigger the start function after this object was
        # moved into its own thread (see QBash constructor).
        self.startWork.connect(self.start)

    @QtCore.pyqtSlot()
    def start(self):
        """
        Poll the Bash output, run it through Pyte, and notify the main applet.
        """
        # Read the shell output until the file descriptor is closed.
        while True:
            try:
                out = os.read(self.fd, 4096)
            except OSError:
                break

            # Feed output into Pyte's state machine and send the new screen
            # output to the GUI thread.
            self.stream.feed(out)
            self.dataReady.emit(self.screen)


class QBash(QtGui.QPlainTextEdit):
    """
    Start ``PollTerminal`` process and render Pyte output as text.
    """
    def __init__(self, *args, numLines=24, numColumns=80, **kwargs):
        super().__init__(*args, **kwargs)

        # Specify the terminal size in terms of lines and columns.
        self.numLines = numLines
        self.numColumns = numColumns

        # Change the 'TERM' environment variable to 'linux' to ensure
        # that Bash does not internally disable the readline library.
        self.envVars = {'TERM': 'linux', 'LANG': 'en_GB.UTF-8'}

        # Use Monospace fonts and disable line wrapping.
        self.setFont(QtGui.QFont('Courier', 9))
        self.setFont(QtGui.QFont('Monospace'))
        self.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)

        # A rough guess on how large to make the window.
        fmt = QtGui.QFontMetrics(self.font())
        width = fmt.width('8') * numColumns
        height = fmt.height() * numLines
        self.resize(width, height + 20)

        # Start the Bash process.
        self.fd = self.forkShell()

        # Create a Qt thread and push the ``PollTerminal`` instance into it.
        self.thread = QtCore.QThread()
        self.pollBash = PollTerminal(self.fd, self.numLines, self.numColumns)
        self.pollBash.dataReady.connect(self.dataReady)
        self.pollBash.moveToThread(self.thread)
        self.thread.start()
        self.pollBash.startWork.emit()

    @QtCore.pyqtSlot(object)
    def keyPressEvent(self, event):
        """
        Redirect all keystrokes to the terminal process.
        """
        # Convert the Qt key to the correct ASCII code.
        code = qbash.util.QtKeyToAscii(event)
        if code is not None:
            os.write(self.fd, code)

    def dataReady(self, screenData):
        """
        Render the new screen as text into the widget.

        This method is triggered via a signal from ``PollTerminal``.
        """
        # Clear the widget and get a handle to its textCursor instance.
        self.clear()
        textCursor = self.textCursor()
        textCursor.setPosition(0)

        # Pyte returns the characters as a list of characters in inside a list
        # of lines. Loop over all of them and insert them in batches with the
        # same fore/back-ground colour. This batch-processing is necessary to
        # minimise the number of Qt insertion calls because they are slow.
        text, lastFg, lastBg = '', 'default', 'default'
        for lineData in screenData:
            for ch in lineData:
                if (ch.fg != lastFg) or (ch.bg != lastBg):
                    # The fore/back-ground col-or for this character is
                    # different from the last one(s) --> insert the accumulated
                    # characters and then start a new batch of characters with
                    # the new fore/back-ground colours.
                    self.insertFormattedText(text, lastFg, lastBg)
                    text, lastFg, lastBg = '', ch.fg, ch.bg
                # Append the current character to the batch.
                text += ch.data
            # Add newline character to the widget because all characters in
            # current line have been processed.
            # and proceed to next line.
            text += '\n'

        # Insert remaining characters except the last newline.
        self.insertFormattedText(text[:-1], lastFg, lastBg)

    def insertFormattedText(self, text, colorFg, colorBg):
        """
        Insert ``text`` into widgets with specified colours.
        """

        # Move cursor to the end and make sure nothing is selected.
        cur = self.textCursor()
        cur.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        cur.clearSelection()

        # Create the desired character format (ie. character colours).
        fg, bg = qbash.util.strToQColorForeground(colorFg, colorBg)
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(fg)
        fmt.setBackground(bg)

        # Insert text with requested colour.
        cur.insertText(text, fmt)

    def forkShell(self):
        """
        Fork the current process and replace it with Bash.
        """
        try:
            childPID, fd = pty.fork()
        except OSError:
            msg = 'Could not spawn another terminal.'
            return None

        if childPID == 0:
            # We are in the child process: flush stdout to be safe.
            sys.stdout.flush()

            # Setup the environment variables for the new terminal.
            for key, value in self.envVars.items():
                os.environ[key] = value

            try:
                # Replace the current process with a new one - the
                # Bash. The first argument to execlp refers to the
                # program, the second to the entry in the process
                # table as listed by eg. 'ps', and the third argument
                # is a command line switch to tell Bash that it should
                # be in interactive mode even though it is not
                # directly connected to a screen (this ensures that
                # it uses the readline library).
                os.execlp('/bin/bash', 'qbash', '-i')
            except:
                print('Error: Could not replace current process with Bash.')
                return None
        else:
            # We are in the parent process.
            print('Spawned Bash shell (PID {})'.format(childPID))
            return fd
