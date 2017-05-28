#!/usr/bin/env python

from fona import _get_output, _send_command, _send_end_signal
from time import sleep

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-28'
__version__ = '1.0'

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
    sleep(0.2)
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
    sleep(0.2)
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
    sleep(0.2)
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
    sleep(0.2)
    _send_command('AT+CSPN')
    return _get_output()

if __name__ == '__main__':
    try:
        print get_carrier_name()
        print 'Sending text...'
        _send_command('AT+CMGF=1')
        sleep(0.2)
        _send_command('AT+CMGS="14127360806"')
        sleep(0.2)
        _send_command('Hello world!')
        sleep(0.2)
        _send_end_signal() # chr(26) is the character for CTRL-Z which is needed to end sending the message
        print 'Text sent'
    except:
        print 'ERROR'
        error = format_exc()
        error_log = open('/home/pi/logs/fona.log', 'w')
        error_log.write(error)
