#!/usr/bin/env python3

from serial import Serial
from time import sleep

import logging

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-24'
__version__ = '1.0'

"""2G FONA Device General Library.

Library applies to 2G FONA UFL GSM US Edition SIM800 Series only. This
library is used for sending commands (see README.md) to the FONA device
in order to execute its predefined instructions (see: https://cdn-shop.
adafruit.com/product-files/1946/SIM800+Series_AT+Command+Manual_V1.09
.pdf). It contains basic methods for writing to and receiving output
from the FONA device.

In order to execute these instructions, the commands must be written to
the FONA device through a serial port; this is done in the send_command
method which is utilized by almost every other method. The serial port
is opened in the /dev/ttyUSB0 port which is where the FONA device should
be plugged for the purpose of this library. To check where the FONA
device is connected if at all, use the Linux terminal command:
    dmesg | grep tty
and search for usb 1-1.5: pl2303 converter now attached to ttyXXXX. If
the XXXX is not USB0, change the serial port creation below to match. If
such a string does not appear, check that the FONA device is connected
to the Raspberry Pi and powered on.

Attributes:
    baud (int): baud rate for FONA device
    fona_port (serial.Serial): serial port where FONA commands are
    written. In this case, the port is located at /dev/ttyUSB0. Since
    this serial port must be written to by multiple threads (SMS_Thread,
    Call_Thread, UI_Thread), there must be a thread lock to ensure only
    one thread has access to this shared port. This port uses the
    previously declared baud as its baud rate and a timeout of 1 second
    logger (logging.logger): logging object to display diagnostic
    information
"""

baud = 9600
fona_port = Serial('/dev/ttyUSB0', baud, timeout=1)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s '
    '%(module)s::%(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
logger = logging.getLogger(__name__)

def send_command(data):
    """Write string command to serial port for the FONA device. See
    README.md for list of commands and their expected outputs/functions.
    Serial ports must write data in the form of bytes, so strings must
    be encoded in unicode (see: https://pythonhosted.org/pyserial/
    pyserial_api.html)

    This method only writes the parameter string to the serial port of
    the FONA device. The parameter for this method can be a command or a
    message whenever an SMS is being sent; however, the former should be
    more frequent.

    Since this library should be used in a multithreaded operating
    system, the invariant for this method is that the parent method
    calling this method should have the thread lock for writing to the
    FONA device serial port.

    NOTE: allow for Raspberry Pi to sleep for at least 0.2 seconds
    between calls of this method to allow for complete write of the data
    parameter. Without a time.sleep(0.2) between calls, data is written
    to the serial port too fast for the FONA to successfully read from.

    Arg:
        data (str): string command. NOTE: \r is appended to commands
    """
    # TODO: fix this so that it tries multiple times to communicate with serial port if unsuccessful the first time
    logger.info('Sending data %s to FONA device' % data)
    fona_port.write((data + '\r').encode('utf-8'))
    sleep(0.2)

def send_eot():
    """Send the signal for CTRL-Z to the FONA device serial port which
    serves as an End of Transmission signal.

    Whenever sending an SMS through the FONA device command line, the
    command AT+CMGF=1 is used in order to set the SMS message format so
    that text entered to the command line is the text used as the
    message to be sent. In order to exit this text mode, CTRL-Z must be
    pressed.

    Since the command line here is emulated through the serial port, the
    text for the command is simply written through the send_command
    method, but the signal for CTRL-Z must be sent by its character
    representation (ASCII character value of 26).
    """
    send_command(chr(26))

def get_output():
    """Obtain and return the output of the FONA device after entering a
    command.

    When sending a command to the FONA device through the command line,
    after a short delay, the device prints to the terminal line(s) of
    output depending on the command entered. This method returns a
    string array of the output of the FONA device after writing a
    desired command.

    Returns:
        String array of output from the FONA device
    """
    output = fona_port.readlines()
    for i in range(len(output)):
        output[i] = output[i].rstrip()
    logger.info('Flushing serial port contents:\n%s' % output)
    return output

def close():
    """Close the serial port."""
    logger.info('Closing FONA serial port')
    fona_port.close()