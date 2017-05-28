#!/usr/bin/env python

from serial import Serial
from sys import exit
from traceback import format_exc

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-24'
__version__ = '1.0'

"""2G FONA Device General Library.

Library applies to 2G FONA UFL GSM US Edition SIM800 Series only. This library
is used for sending commands (see README.md) to the FONA device in order to
execute its predefined instructions (see: https://cdn-shop.adafruit.com/product-
files/1946/SIM800+Series_AT+Command+Manual_V1.09.pdf). It contains methods which
simplify communicating with the FONA device: checking if a successful connection
can be established with the FONA device, sending commands to the device,
checking the output of the device after commands, methods for basic commands
such as checking FONA model and revision, etc.

In order to execute these instructions, the commands must be written to the FONA
device through a serial port; this is done in the _send_command method which is
utilized by almost every other method. The serial port is opened in the
/dev/ttyUSB0 port which is where the FONA device should be plugged for the
purpose of this library. To check where the FONA device is connected if at all,
use the Linux terminal command:
    dmesg | grep tty
and search for usb 1-1.5: pl2303 converter now attached to ttyXXXX. If the XXXX
is not USB0, change the serial port creation below to match. If such a string
does not appear, check that the FONA device is connected to the Raspberry Pi
and powered on.

Attributes:
    baud (int): baud rate for FONA device
    fona_port (serial.Serial): serial port where FONA commands are written. In
    this case, the port is located at /dev/ttyUSB0. Since this serial port must
    be written to by multiple threads (SMS_Thread, Call_Thread, UI_Thread),
    there must be a thread lock to ensure only one thread has access to this
    shared port. This port uses the previously declared baud as its baud rate
    and a timeout of 1 second
"""

baud = 9600
fona_port = Serial('/dev/ttyUSB0', baud, timeout=1)

def _send_command(data):
    """Write string command to serial port for the FONA device. See README.md
    for list of commands and their expected outputs/functions. Serial ports must
    write data in the form of bytes, so strings must be encoded in unicode (see:
    https://pythonhosted.org/pyserial/pyserial_api.html)

    This helper method only writes the parameter string to the serial port of
    the FONA device. The parameter for this method can be a command or a
    message whenever an SMS is being sent; however, the former should be more
    frequent.

    Since this library should be used in a multithreaded operating system, the
    invariant for this method is that the parent method calling this helper
    should have the thread lock for writing to the FONA device serial port.

    Arg:
        data (str): string command. NOTE: \r is appended to commands
    """
    data += '\r'
    fona_port.write(data.encode('utf-8'))

def _send_end_signal():
    """Send the signal for CTRL-Z to the FONA device serial port.

    Whenever sending an SMS through the FONA device command line, the command
    AT+CMGF=1 is used in order to set the SMS message format so that text
    entered to the command line is the text used as the message to be sent. In
    order to exit this text mode, CTRL-Z must be pressed.

    Since the command line here is emulated through the serial port, the text
    for the command is simply written through the _send_command method, but the
    signal for CTRL-Z must be sent by its character representation (ASCII
    character value of 26).
    """
    _send_command(chr(26))

def _get_output():
    """Obtain and return the output of the FONA device after entering a command.
    
    When sending a command to the FONA device through the command line, after a
    short delay, the device prints to the terminal line(s) of output depending
    on the command entered. This method returns a string array of the output of
    the FONA device after writing a desired command.

    Returns:
        String arry of output from the FONA device
    """
    output = fona_port.readlines()
    for i in range(len(output)):
        output[i] = output[i].rstrip()
    return output

def check_connection():
    """Checks if the FONA 2G device can be connected to successfully.

    This is accomplished by sending the AT command to the FONA device serial
    port. Whenever this command is sent, 'OK' will be outputted to the serial
    port if there is a successful connection.

    If connecting to the FONA device is unsuccessful, the FONA device will not
    output OK after which this method will raise an IOError which signals to the
    caller that there was not a successful connection. This method should be
    called first in any series of methods that interact with the FONA device to
    initially ensure a proper connection exists.

    Raises:
        IOError if the Raspberry Pi cannot connect to the FONA device
    """
    _send_command('AT')
    output = _get_output()
    if 'OK' in output:
        print '\n***\n*** SUCCESSFUL connecting to FONA\n***\n'
    else:
        print '\n***\n*** UNSUCCESSFUL connecting to FONA\n***\n'
        raise IOError('\n***\n*** Unable connecting to FONA\n***\n')

def get_model():
    """Send ATI command to output the FONA identification information.

    This method first checks if there is a successful connection between the
    Raspberry Pi and the FONA device. If so, the command for outputting FONA
    identification information is sent, and the output of the FONA
    is then returned; if a successful connection was not obtained, the
    method raises the IOError to the caller.

    Returns:
        String of FONA model and revision
    """
    check_connection()
    _send_command('ATI')
    return _get_output()

def get_simcard_number():
    """Send AT+CCID command to output the SIM card identifier (outputs
    Integrated Circuit Card ID (CCID)).

    First checks if there is a successful connection. If so, the command for
    outputting SIM card number is sent, and the output of the FONA
    is then returned; if a successful connection was not obtained, the
    method raises the IOError to the caller.

    Returns:
        String of SIM card identifier
    """
    check_connection()
    _send_command('AT+CCID')
    return _get_output()

def get_reception():
    """Send AT+CSQ command to output the reception of the FONA

    First checks if there is a successful connection. If so, the command for
    outputting reception is sent, and the output of the FONA is then returned.
    The output of the FONA device after sending this command should be in the
    format:
        ['AT+CSQ', '+CSQ: X,0', '', 'OK']
    where the X determines the strength of the reception: a higher number means
    a stronger reception. If a successful connection was not obtained, the
    method raises the IOError to the caller.

    Returns:
        String of reception
    """
    check_connection()
    _send_command('AT+CSQ')
    return _get_output()
    
def get_carrier_name():
    """Send AT+CSPN command to output the name of the carrier.

    First checks if there is a successful connection. If so, the command for
    outputting carrier name is sent, and the output of the FONA is then
    returned. If using a non-major carrier, it is possible for this method to
    return a string array which contains the string ERROR. If this is the case,
    this error string should be disregarded. If a successful connection was not
    obtained, the method raises the IOError to the caller.

    Returns:
        String of carrier name
    """
    check_connection()
    _send_command('AT+CSPN')
    return _get_output()

def close():
    """Close the serial port for the FONA device."""
    fona_port.close()
