#!/usr/bin/env python3

from PyQt5 import QtWidgets, uic

import sys
import threading
import traceback
import time
import os
from source_handler import InvalidFrame, SerialHandler
os.environ.__setitem__('DISPLAY', ':0.0')

stop_reading = threading.Event()

can_messages = {}
can_messages_lock = threading.Lock()

thread_exception = None

baudrate = 115200
serial_device = "/dev/ttyUSB0"

def reading_loop(source_handler):
    """Background thread for reading."""
    try:
        while not stop_reading.is_set():
            try:
                frame_id, data = source_handler.get_message()
            except InvalidFrame:
                continue
            except EOFError:
                break

            # Add the frame to the can_messages dict and tell the main thread to refresh its content
            with can_messages_lock:
                try:
                    root.RadioName.setText("placeholder")
                except:
                    print ("pété")

                can_messages[frame_id] = data
                print ("FRAME ID %s  :  %s" % (frame_id, format_data_ascii(data)))
                if frame_id == 0x02 :
                    root.Temperature.setText(format_data_ascii(data))

                if frame_id == 0x04 :
                    root.RadioName.setText(format_data_ascii(data))

        stop_reading.wait()

    except:
        if not stop_reading.is_set():
            # Only log exception if we were not going to stop the thread
            # When quitting, the main thread calls close() on the serial device
            # and read() may throw an exception. We don't want to display it as
            # we're stopping the script anyway
            global thread_exception
            thread_exception = sys.exc_info()

def format_data_hex(data):
    """Convert the bytes array to an hex representation."""
    # Bytes are separated by spaces.
    return ' '.join('%02X' % byte for byte in data)


def format_data_ascii(data):
    """Try to make an ASCII representation of the bytes.

    Non printable characters are replaced by '?' except null character which
    is replaced by '.'.
    """
    msg_str = ''
    for byte in data:
        char = chr(byte)
        if char == '\0':
            msg_str = msg_str + '.'
        elif ord(char) < 32 or ord(char) > 126:
            msg_str = msg_str + '?'
        else:
            msg_str = msg_str + char
    return msg_str


def parse_ints(string_list):
    int_set = set()
    for line in string_list:
        try:
            int_set.add(int(line, 0))
        except ValueError:
            continue
    return int_set


def run():
    source_handler = SerialHandler(serial_device, baudrate)
    reading_thread = None

    try:
        # If reading from a serial device, it will be opened with timeout=0 (non-blocking read())
        source_handler.open()

        # Start the reading background thread
        reading_thread = threading.Thread(target=reading_loop, args=(source_handler,))

        app = QtWidgets.QApplication(sys.argv)  # Create an instance of QtWidgets.QApplication
        root = Ui()  # Create an instance of our class
        reading_thread.start()
        # root.RadioName.setText("placeholder")
        app.exec_()  # Start the application

    finally:
        # Cleanly stop reading thread before exiting
        if reading_thread:
            stop_reading.set()

            if source_handler:
                source_handler.close()

            reading_thread.join()

            # If the thread returned an exception, print it
            if thread_exception:
                traceback.print_exception(*thread_exception)
                sys.stderr.flush()

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self) # Load the .ui file
        self.show() # Show the GUI

if __name__ == '__main__':
    run()