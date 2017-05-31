#!/usr/bin/env python

from fona import _get_output, _send_command, _send_end_signal
from time import sleep
from traceback import format_exc

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-28'
__version__ = '1.0'

"""General Purpose Library for 2G FONA Device.

Using the methods defined in fona.py, this library allows for full use of the
FONA device by sending specific commands to perform tasks such as receive SMS,
send SMS, check FONA battery percentage, etc.

NOTE: whenever calling the fona._send_command method, it is necessary to call
time.sleep(0.2) after in order to ensure that the command being sent will be
written completely. Without waiting, the serial port may be written to too
frequently, resulting in incomplete command entries and unintended output/error.
"""

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
    if 'OK' in _get_output():
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
    """Send AT+CSQ command to output the reception of the FONA.

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

def get_battery_percentage():
    """Send AT+CBC command to output the battery percentage of the FONA device.

    First this method checks the connection from the FONA device to the
    Raspberry Pi. Then this device sends the command to output the battery
    percentage of the FONA device which is then returned as a string array.

    Returns:
        Battery percentage of the FONA device in a string array in the form:
            ['AT+CBC', '+CBC: 0,100,4220', '', 'OK']
        where the percentage is the number between the 0 and 4220 (in this case,
        the FONA device is 100% charged)
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CBC')
    return _get_output()

def send_message(number, message):
    """Send an SMS to the phone number which is given by the string parameter
    number.
    
    To send an SMS, first the connection with the FONA is checked. If
    successful, the AT command for changing the message type (AT+CMGF) is
    written to the FONA device. When entering this command in the FONA terminal,
    this allows the text directly typed in the terminal to be used as the
    message to be sent. The command for setting the phone number to be texted is
    written, using the number parameter, followed by writing the message to the
    FONA device; this is why changing the text type was required. Finally the
    CTRL-Z signal is sent, escaping the direct message entry and sending the
    message to the desired recipient.

    Args:
        number (str): string of the phone number to send the message to
        message (str): the message to be sent to the phone number
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CMGF=1')
    sleep(0.2)
    _send_command('AT+CMGS="' + number + '"')
    sleep(0.2)
    _send_command(message)
    sleep(0.2)
    _send_end_signal()

def message_received():
    """Determines if any new messages have been sent to the FONA device.

    To determine if any new message has been received, this method first checks
    FONA connection. If successful, it writes to the FONA serial port the AT
    command which outputs the number of total messages received. The _get_output
    method will return a string array whose second index contains the number of
    received messages.

    This value is the total number of messages received, according to the FONA
    device; however, it is not the total number of messages accounted for (or
    recorded). To save the number of messages accounted for (non-new), we save
    the current value of messages received to a file (if it's greater than the
    number of recorded messages). Initially, this file will be empty, so the
    value for this variable is assumed to be zero.

    At any point in calling this method, the number of messages received will
    always be greater than or equal to the number of messages recorded. If the
    number of messages received by the FONA is greater than the number of
    messages recorded, then new messages have been received. This is why the
    max of number of messages received and number recorded is the new value for
    number of messages recorded.

    This method returns the difference between number of messages received by
    the FONA and number of messages recorded. If no new messages have been
    received, the number of messages received and the number of messages
    recorded will be equal, meaning this method will return zero to indicate no
    new messages; otherwise this method will return the number of new messages.

    Returns:
        If any new messages have been received, this method returns non zero
        (the number of new messages unaccounted for); otherwise it returns zero
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[1].split(',')[1])
    f = open('sms_record.txt', 'r')
    try:
        sms_recorded = int(f.readline())
    except ValueError:
        """empty file"""
        sms_recorded = 0
    f = open('sms_record.txt', 'w+')
    f.write(str(max(sms_received, sms_recorded)))
    return sms_received - sms_recorded

def parse_message(output):
    """Parses the message payload from the FONA device output after sending it
    its command for outputting the full details of an SMS received.
    
    In the get_all_sms method, this method is called only after one command has
    been sent to the FONA device. This is done in order to know for certain how
    much to offset the for loop by to parse the message. If more than one
    command was entered into the FONA serial port, the offset would have to
    begin at two times the number of previously entered commands; in order to
    work around this issue, exactly one command should be written to the serial
    port before this method is called.

    In the get_n_newest and get_n_oldest methods, multiple commands are written
    to the FONA port, but before the command to output a specific SMS is
    written, the FONA port is flushed by calling the _get_output method.

    In order to extract the message from the output, this message only
    concatenates elements of the string output. The output string array is in
    the format:
        [AT+CMGR=2', '+CMGR: "REC READ", "+XXXXXXXXXXX","","17/05/28,
        14:33:14-16",145,4,0,0,"+12063130055", 145,5', 'Hello', '', 'OK']
    where elements are indicated by single quotes.

    The SMS begins in the second array entry and ends at the third to last, with
    empty entries signaling a new line in the message.


    ['AT+CMGF=1', 'OK', 'AT+CSDH=1', 'OK', 'AT+CMGR=2', '+CMGR: "REC READ",
        "+14127360806","","17/05/28,14:33:14-16",145,4,0,0,"+12063130055",
        145,5', 'Hello', '', 'OK']
    """
    message = ""
    message_reached = False
    for string in output:
        if message_reached and string != 'OK':
            message += string + '\n'
        if '+CMGR:' in string:
            message_reached = True
    return message[:-2]

def get_all_sms():
    """Returns array of (number, timestamp, message) tuples for all messages received.
    
    In order to get received messages, first the command for outputting the
    number of total messages received is written to the FONA port, and the
    output is saved.
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CMGF=1') # display message in output
    sleep(0.2)
    _send_command('AT+CSDH=1') # detailed SMS output
    sleep(0.2)
    _send_command('AT+CPMS?')
    num = int(_get_output()[5].split(',')[1]) # 5 because other commands were entered
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, num + 1):
        sleep(0.2)
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(parse_message(output))
    return messages

def get_new_sms():
    num_new = message_received()
    sleep(0.2)
    _send_command('AT+CMGF=1') # display message in output
    sleep(0.2)
    _send_command('AT+CSDH=1') # detailed SMS output
    sleep(0.2)
    _send_command('AT+CPMS?')
    num = int(_get_output()[5].split(',')[1]) # 5 because other commands were entered
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(num - num_new + 1, num + 1):
        sleep(0.2)
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+', ''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(parse_message(output))
    return messages

def get_n_newest_sms(n):
    check_connection()
    sleep(0.2)
    _send_command('AT+CPMS?')
    num = int(_get_output()[1].split(',')[1]) # 1 because other command was entered
    if n > num or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    sleep(0.2)
    _send_command('AT+CMGF=1') # display message in output
    sleep(0.2)
    _send_command('AT+CSDH=1') # detailed SMS output
    _get_output() # clear FONA output
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(num - n + 1, num + 1):
        sleep(0.2)
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(parse_message(output))
    return messages

def get_n_oldest_sms(n):
    check_connection()
    sleep(0.2)
    _send_command('AT+CPMS?')
    num = int(_get_output()[1].split(',')[1]) # 1 because other command was entered
    if n > num or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    sleep(0.2)
    _send_command('AT+CMGF=1') # display message in output
    sleep(0.2)
    _send_command('AT+CSDH=1') # detailed SMS output
    _get_output() # clear FONA output
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, n + 1):
        sleep(0.2)
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(parse_message(output))
    return messages

if __name__ == '__main__':
    print get_n_oldest_sms(1)['message'][0]
    print 'here'
