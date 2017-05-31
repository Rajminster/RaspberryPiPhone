#!/usr/bin/env python

from fona import _get_output, _send_command, _send_end_signal
from time import sleep

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

def _parse_message(output):
    """Parses the message payload from the FONA device output after sending it
    its command for outputting the full details of an SMS received.

    In order to tell when the message begins, this method must begin iterating
    over the output parameter given. Since any number of commands at least one
    could have been written to the FONA before this method has been called, the
    only way to determine where the message begins is the iterate until the
    string denoting message status type (string beginning with +CMGR:) is found;
    the next string is the beginning of the message.
    
    The output parameter could have the format:
        [AT+CMGR=2', '+CMGR: "REC READ", "+XXXXXXXXXXX","","17/05/28,
        14:33:14-16",145,4,0,0,"+12063130055", 145,5', 'Hello', '', 'OK']
    where elements are indicated by single quotes and the X's make up the phone
    number of the sender. Here, the SMS begins in the second array entry and
    ends at the third to last, with empty entries indicating a new line within
    the message. The OK string is a signal from the FONA device that the command
    has successfully finished.

    Arg:
        output (str list): string array outputted from the FONA device serial
        port and given by the _get_output method

    Returns:
        The SMS received in one string as it was sent
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
    """Returns array of number, timestamp, message tuples for all messages
    received by the FONA device with successful connection to Raspberry Pi.
    
    In order to get any message received with useful metadata, first two
    commands must be sent to the FONA device: AT+CMGF=1 which sets SMS message
    format to text and AT+CSDH=1 which shows SMS text mode metadata (timestamp
    received, sender phone number, message contents, etc.).

    With this setup, the AT+CPMS command is sent which outputs the total number
    of SMS received which is used to iterate through each message received. To
    output the ith message received, the AT+CMGR=i command is sent, and with the
    first two commands sent, the FONA device outputs clear metadata about the
    SMS which is appended to the array to be returned.

    In this method, the total number of messages received is indexed as the
    fifth element of the _get_output string array because before the AT+CPMS?
    command was entered, two other commands were entered which each take two
    indices in the array. NOTE: the FONA device does not use zero-indexing when
    outputting messages received.

    Returns:
        Array of sender phone number, SMS timestamp, and message tuples of all
        messages received by the FONA device
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CMGF=1')
    sleep(0.2)
    _send_command('AT+CSDH=1')
    sleep(0.2)
    _send_command('AT+CPMS?')
    sleep(0.2)
    sms_received = int(_get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        sleep(0.2)
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_new_sms():
    """Returns array of number, timestamp, message tuples for all messages which
    have been recently received by the FONA which have just been accounted for
    in the message_received method.
    
    This method first calls the message_received method which ensures a
    successful connection exists between the FONA device and the Raspberry Pi
    as well as find out how many messages have been marked as 'new'. After this,
    the method writes the AT+CMGF=1 command to set the SMS message format to
    text to make message output legible. Next it writes the AT+CSDH=1 command
    which makes the FONA console output more detailed metadata about messages
    received.

    The command to output the total number of messages received is then entered
    to only grab the newest received to return. This value is obtained by
    indexing into the fifth element of the _get_output string array because it's
    the output of the third command entered; since each command requires two
    indices of the _get_output array (one for the command and one for its
    output), it's the sixth place (5 when zero-indexed).
    
    Now the method iterates through the new messages received and appends those
    to the array to be returned with metadata phone number of sender, timestamp
    of message, and message contents. NOTE: the FONA does not zero-index
    messages received, so 1 is added to the lower and upper bound of the for
    loop.

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for new messages received
    """
    new_received = message_received()
    sleep(0.2)
    _send_command('AT+CMGF=1')
    sleep(0.2)
    _send_command('AT+CSDH=1')
    sleep(0.2)
    _send_command('AT+CPMS?')
    sleep(0.2)
    sms_received = int(_get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - new_received + 1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        sleep(0.2)
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+', ''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_newest_sms(n):
    """Returns array of sender phone number, timestamp, and message content
    tuples of the n newest received messages.

    This is accomplished by first checking for an existing connection between
    the Raspberry Pi and the FONA device. This method then writes the AT+CPMS?
    command to output the total number of messages received in order to error
    check the n argument. After this, commands for setting SMS message format
    and output detailed SMS metadata are entered (AT+CMGF=1 and AT+CSDH=1,
    respectively). Because the output from these two commands are not necessary,
    this method calls the _get_output method in order to flush the FONA serial
    port's output.

    Now the method iterates through the n newest messages and appends their
    sender phone number, message timestamp, and message contents to the array it
    will return. NOTE: the FONA does not zero-index messages received, so 1 is
    added to the lower and upper bounds of the for loop.

    Arg:
        n (int): the number of newest messages to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the number
        of messages received

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for newest messages received
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    sleep(0.2)
    _send_command('AT+CMGF=1')
    sleep(0.2)
    _send_command('AT+CSDH=1')
    sleep(0.2)
    _get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - n + 1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        sleep(0.2)
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_oldest_sms(n):
    """Returns array of sender phone number, timestamp, and message content
    tuples of the n oldest received messages.

    This is accomplished by first checking for an existing connection between
    the Raspberry Pi and the FONA device. This method then writes the AT+CPMS?
    command to output the total number of messages received in order to error
    check the n argument. After this, commands for setting SMS message format
    and output detailed SMS metadata are entered (AT+CMGF=1 and AT+CSDH=1,
    respectively). Because the output from these two commands are not necessary,
    this method calls the _get_output method in order to flush the FONA serial
    port's output.

    Now the method iterates through the n oldest messages and appends their
    sender phone number, message timestamp, and message contents to the array it
    will return. NOTE: the FONA does not zero-index messages received, so 1 is
    added to the lower and upper bounds of the for loop.

    Arg:
        n (int): the number of oldest messages to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the number
        of messages received

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for oldest messages received
    """
    check_connection()
    sleep(0.2)
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    sleep(0.2)
    _send_command('AT+CMGF=1')
    sleep(0.2)
    _send_command('AT+CSDH=1')
    sleep(0.2)
    _get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, n + 1):
        _send_command('AT+CMGR=' + str(i))
        sleep(0.2)
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages
