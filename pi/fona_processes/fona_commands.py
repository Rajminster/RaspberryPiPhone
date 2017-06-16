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
        print '\n***\n*** SUCCESSFUL connecting to FONA\n***'
    else:
        print '\n***\n*** UNSUCCESSFUL connecting to FONA\n***'
        raise IOError('\n***\n*** Unable connecting to FONA\n***')

def check_output(output):
    """Checks if the FONA 2G device can be connected to successfully.

    This is accomplished by checking if the output of entering a command results
    in a string array whose last entry is the string OK.

    Raises:
        IOError if the Raspberry Pi cannot connect to the FONA device
    """
    if output[len(output) - 1] != 'OK':
        print '\n***\n*** UNSUCCESSFUL connecting to FONA\n***'
        raise IOError('\n***\n*** Unable connecting to FONA\n***')
    print '\n***\n*** SUCCESSFUL connecting to FONA\n***'

def get_time():
    """
    """
    check_connection()
    _send_command('AT+CIPGSMLOC=1,1')
    return _get_output()

def get_lat_long():
    """
    """
    check_connection()
    _send_command('AT+CIPGSMLOC=1,1')
    return _get_output()

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
    _send_command('ATI')
    output = _get_output()
    check_output(output)
    return output

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
    _send_command('AT+CSQ')
    return _get_output()[1].split(',')[0].split(' ')[1]

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
    _send_command('AT+CBC')
    return _get_output()

def send_sms(number, message):
    """Send an SMS to the phone number which is given by the string parameter
    number.

    To send an SMS, first the connection with the FONA is checked. If
    successful, the AT command for changing the message type (AT+CMGF) is
    written to the FONA device. When entering this command in the FONA terminal,
    this allows the text directly typed in the terminal to be used as the
    SMS to be sent. The command for setting the phone number to be texted is
    written, using the number parameter, followed by writing the message to the
    FONA device; this is why changing the text type was required. Finally the
    CTRL-Z signal is sent, escaping the direct message entry and sending the
    message to the desired recipient.

    Args:
        number (str): string of the phone number to send the message to. NOTE:
        the number which is the intended recipient must have the appropriate
        international code
        message (str): the message part of the SMS to be sent to the phone
        number
    """
    check_connection()
    _send_command('AT+CMGF=1')
    _send_command('AT+CMGS="' + number + '"')
    _send_command(message)
    _send_end_signal()

def sms_received():
    """Determines if any new SMSs have been sent to the FONA device.

    To determine if any new SMS has been received, this method first checks FONA
    connection. If successful, it writes to the FONA serial port the AT command
    which outputs the number of total SMSs received. The _get_output method
    will return a string array whose second index contains the number of
    received SMSs.

    This value is the total number of SMSs received, according to the FONA
    device; however, it is not the total number of SMSs accounted for (or
    recorded). To save the number of SMSs accounted for (non-new), we save the
    current value of SMSs received to a file (if it's greater than the number of
    recorded SMSs). Initially, this file will be empty, so the value for this
    variable is assumed to be zero.

    At any point in calling this method, the number of SMSs received will always
    be greater than or equal to the number of SMSs recorded. If the number of
    SMSs received by the FONA is greater than the number of SMSs recorded, then
    new SMSs have been received. This is why the max of number of SMSs received
    and number recorded is the new value for number of SMSs recorded.

    This method returns the difference between number of SMSs received by the
    FONA and number of SMSs recorded. If no new SMSs have been received, the
    number of SMSs received and the number of SMSs recorded will be equal,
    meaning this method will return zero to indicate no new SMSs; otherwise this
    method will return the number of new SMSs.

    Returns:
        If any new SMSs have been received, this method returns non zero (the
        number of new SMSs unaccounted for); otherwise it returns zero
    """
    check_connection()
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
    """Returns array of number, timestamp, message tuples for all SMSs received
    by the FONA device with successful connection to Raspberry Pi.

    In order to get any SMS received with useful metadata, first two commands
    must be sent to the FONA device: AT+CMGF=1 which sets SMS message format to
    text and AT+CSDH=1 which shows SMS text mode metadata (timestamp received,
    sender phone number, message contents, etc.).

    With this setup, the AT+CPMS command is sent which outputs the total number
    of SMSs received which is used to iterate through each SMS received. To
    output metadata about the ith SMS received, the AT+CMGR=i command is sent,
    and with the first two commands sent, the FONA device outputs clear metadata
    about the ith SMS which is appended to the tuple array to be returned.

    In this method, the total number of SMSs received is indexed as the fifth
    element of the _get_output string array because before the AT+CPMS? command
    was entered, two other commands were entered which each take two indices in
    the array. NOTE: the FONA device does not use zero-indexing when outputting
    SMSs received.

    Returns:
        Array of sender phone number, SMS timestamp, and message tuples of all
        SMSs received by the FONA device
    """
    check_connection()
    _send_command('AT+CMGF=1')
    _send_command('AT+CSDH=1')
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_new_sms():
    """Returns array of number, timestamp, message tuples for all SMSs which
    have been recently received by the FONA which have just been accounted for
    in the sms_received method.

    This method first calls the sms_received method which ensures a successful
    connection exists between the FONA device and the Raspberry Pi as well as
    find out how many SMSs have been marked as 'new'. After this, the method
    writes the AT+CMGF=1 command to set the SMS message format to text to make
    message output legible. Next it writes the AT+CSDH=1 command which makes the
    FONA console output more detailed metadata about SMSs received.

    The command to output the total number of SMSs received is then entered to
    only grab the newest received to return. This value is obtained by indexing
    into the fifth element of the _get_output string array because it's the
    output of the third command entered; since each command requires two indices
    of the _get_output array (one for the command and one for its output), it's
    the sixth place (5 when zero-indexed).

    Now the method iterates through the new SMSs received and appends those
    to the array to be returned with metadata phone number of sender, timestamp
    of message, and message contents. NOTE: the FONA does not zero-index SMSs
    received, so 1 is added to the lower and upper bound of the for loop.

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for new SMSs received
    """
    new_received = message_received()
    _send_command('AT+CMGF=1')
    _send_command('AT+CSDH=1')
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - new_received + 1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+', ''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_newest_sms(n):
    """Returns array of sender phone number, timestamp, and message content
    tuples of the n newest received SMSs.

    This is accomplished by first checking for an existing connection between
    the Raspberry Pi and the FONA device. This method then writes the AT+CPMS?
    command to output the total number of SMSs received in order to error check
    the n argument. After this, commands for setting SMS message format and
    output detailed SMS metadata are entered (AT+CMGF=1 and AT+CSDH=1,
    respectively). Because the output from these two commands are not necessary,
    this method calls the _get_output method in order to flush the FONA serial
    port's output.

    Now the method iterates through the n newest SMSs and appends their sender
    phone number, message timestamp, and message contents to the array it will
    return. NOTE: the FONA does not zero-index SMSs received, so 1 is added to
    the lower and upper bounds of the for loop.

    Arg:
        n (int): the number of newest SMSs to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the number
        of SMSs received

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for newest SMSs received
    """
    check_connection()
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    _send_command('AT+CMGF=1')
    _send_command('AT+CSDH=1')
    _get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - n + 1, sms_received + 1):
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_oldest_sms(n):
    """Returns array of sender phone number, timestamp, and message content
    tuples of the n oldest received SMSs.

    This is accomplished by first checking for an existing connection between
    the Raspberry Pi and the FONA device. This method then writes the AT+CPMS?
    command to output the total number of SMSs received in order to error check
    the n argument. After this, commands for setting SMS message format and
    output detailed SMS metadata are entered (AT+CMGF=1 and AT+CSDH=1,
    respectively). Because the output from these two commands are not necessary,
    this method calls the _get_output method in order to flush the FONA serial
    port's output.

    Now the method iterates through the n oldest SMSs and appends their sender
    phone number, message timestamp, and message contents to the array it will
    return. NOTE: the FONA does not zero-index SMSs received, so 1 is added to
    the lower and upper bounds of the for loop.

    Arg:
        n (int): the number of oldest SMSs to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the number
        of SMSs received

    Returns:
        Array of sender phone number, message timestamp, and message contents
        tuples for oldest SMSs received
    """
    check_connection()
    _send_command('AT+CPMS?')
    sms_received = int(_get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    _send_command('AT+CMGF=1')
    _send_command('AT+CSDH=1')
    _get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, n + 1):
        _send_command('AT+CMGR=' + str(i))
        output = _get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def phone_status():
    """Output the status of the phone activity.

    To output the status, this method first checks the connection between the
    Raspberry Pi and the FONA device. If there exists a secure connection, then
    this method will send the command AT+CPAS which makes the FONA device output
    the status of the phone. Depending on the output of this method, it can be
    determined if there is an incoming call to the FONA, no calls, or a call in
    process.

    After writing the AT+CPAS command to the FONA device, its output is in the
    format:
        ['AT+CPAS', '+CPAS: 0', '', 'OK']
    So the second element of the string array, second element on the split of
    whitespace is returned. If this value is a 0, then this means there are no
    calls occurring or incoming. 2 means the status is unknown. 3 means there is
    an incoming call, 4 means there is a call in progress.

    Returns:
        String of the current status of phone activity. Values can only be 0, 2,
        3, or 4
    """
    check_connection()
    _send_command('AT+CPAS')
    return _get_output()[1].split(' ')[1]

def call_number(number):
    """Call the phone number parameter.

    First check for a successful connection between the FONA device and the
    Raspberry Pi. If this check is successful, then send the command for
    calling a phone number.

    Arg:
        number (str): string of the phone number to call. NOTE: this phone
        number should contain an international code.
    """
    check_connection()
    _send_command('ATD' + number + ';')

def answer_call():
    """Answer incoming call to this FONA device.

    If a call is incoming, this method will send the ATA command which instructs
    the FONA device to answer that call.
    """
    check_connection()
    _send_command('ATA')

def end_call():
    """Ends any current call in process.

    Ends call in process by sending the ATH command. Since this method should be
    called whenever a call is in process, this method does not check for
    successful connection with the FONA device."""
    _send_command('ATH')

def mute_call():
    """Mutes any call in process.

    Turns on muting for the current call in process. This method will only mute
    a call if a call is in process.
    """
    _send_command('AT+CMUT=1')

def unmute_call():
    """Turns off mute setting for a current call in process.

    This method will only turn off the mute setting for a call that is in
    process and will not do anything otherwise.
    """
    _send_command('AT+CMUT=0')

def start_audio(file_path):
    """TODO: instead of 50 default volume, save volume to a file"""
    """Use the FONA device to begin playing an audio file, given its file path.

    In order to play an audio file with the FONA device, a call cannot be in
    progress. If this is the case, the command AT+CMEDPLAY=1 along with the
    file path for the device, channel, and volume is written to the FONA device.
    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    For the channel parameter, this method passes 0 for the main channel; 1
    would be used for an aux channel.

    This method's intended purpose is to play voicemail files.

    Arg:
        file_path (str): location of the audio file to be played
    """
    check_connection()
    _send_command('AT+CMEDPLAY=1,' + file_path + ',0,50')

def stop_audio(file_path):
    """Stop playing any audio file currently playing.

    This method writes to the FONA device serial port the command for stopping
    the audio file located at the given file path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    check_connection()
    _send_command('AT+CMEDPLAY=0,' + file_path + ',0,50')

def pause_audio(file_path):
    """Pause a playing audio file currently playing.

    This method writes to the FONA device serial port the command for only
    pausing a playing audio file located at the given file path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    check_connection()
    _send_command('AT+CMEDPLAY=2,' + file_path + ',0,50')

def play_audio(file_path):
    """Continue playing an audio file wherever it has been left off.

    This method only writes to the FONA device port the command to continue
    playing whichever audio file is saved at the given file path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    check_connection()
    _send_command('AT+CMEDPLAY=3,' + file_path + ',0,50')

def set_audio_file_volume(volume):
    """Sets the volume for playing an audio file only.

    To set the volume used whenever an audio file is being played, this method
    writes to the FONA port the command.

    Arg:
        volume (int): the volume level to be set (must be between 0 and 100
        inclusive)

    Raises:
        ValueError if the value for volume is less than 0 or greater than 100
    """
    if volume < 0 or volume > 100:
        raise ValueError('\n***\n*** Out of range value for volume\n***')
    check_connection()
    _send_command('AT+CMEDIAVOL=' + volume)

def start_voice_recording():
    """
    """
    check_connection()
    # format: AT+CREC=1, file_path, 1 (for WAV format), 0 (use int value for how long you want the recording to be), 0 (for FAT format), 3 (highest quality), 0 (MIC1)
    _send_command('AT+CREC=1')

def set_speaker_volume(volume):
    """Set volume for Raspberry Pi speakers.

    Unlike the set_audio_file_volume method, this method sets the volume for
    the entire phone's speakers. To do so, this method writes the ATL command
    with the given volume parameter to the FONA device.

    Arg:
        volume (int): volume of the speakers to be set

    Raises:
        ValueError if the value for volume is less than 0 or greater than 9
    """
    if volume < 0 or volume > 9:
        raise ValueError('\n***\n*** Out of range value for volume\n***')
    check_connection()
    _send_command('ATL' + volume)

def echo_on():
    check_connection()
    _send_command('ATE1')

def echo_off():
    check_connection()
    _send_command('ATE0')

def factory_reset():
    check_connection()
    _send_command('AT&F0')

def enable_caller_id():
    check_connection()
    _send_command('AT+CLIP=1')

def disable_caller_id():
    check_connection()
    _send_command('AT+CLIP=0')

def set_ringtone_volume(volume):
    if volume < 0 or volume > 100:
        raise ValueError('\n***\n*** Out of range value for volume\n***')
    check_connection()
    _send_command('AT+CRSL=' + volume)

def power_off():
    check_connection()
    _send_command('AT+CPOWD=1')

def get_local_timestamp():
    check_connection()
    _send_command('AT+CLTS?')

def get_service_provider():
    check_connection()
    _send_command('AT+CSPN?')

def open_microphone():
    check_connection()
    _send_command('AT+CEXTERN=0')

def close_microphone():
    check_connection()
    _send_command('AT+CEXTERN=1')

def initiate_tcp_connection(ip_address):
    check_connection()
    # 'AT+CIPSTART=2'

def send_through_tcp(ip_address):
    check_connection()
    # 'AT+CIPSEND=2'

def close_connection():
    check_connection()
    # 'AT+CIPCLOSE=0'

def get_local_ip():
    check_connection()
    _send_command('AT+CIFSR')

def gsm_location():
    check_connection()
    _send_command('AT+CIPGSMLOC=1')

def set_sender_address(address, name):
    check_connection()
    _send_command('AT+SMTPFROM=' + address + ',' + name)

def set_recipient_address(address, name):
    check_connection()
    _send_command('AT+SMTPRCPT=' + address + ',' + name)

def set_email_subject(subject):
    check_connection()
    _send_command('AT+SMTPSUB=' + subject)

def set_email_body(body):
    check_connection()
    _send_command('AT+SMTPBODY=' + str(len(body)))
    _send_command(body)

def email_txt_file(file_name, length):
    # NOTE: length is the maximum length of a TXT file name
    check_connection()
    _send_command('AT+SMTPFILE=1,' + file_name + ',' + length + ',0')

def send_email():
    check_connection()
    _send_command('AT+SMTPSEND')

def set_pop3_server_account(server, user, password):
    check_connection()
    _send_command('AT+POP3SRV=' + server + ',' + user + ',' + password)

def pop_log_in():
    check_connection()
    _send_command('AT+POP3IN')

def get_email_num_size():
    check_connection()
    _send_command('AT+POP3NUM')

def get_email_size(number):
    check_connection()
    _send_command('AT+POP3LIST=' + number)

def set_delete_email(number):
    check_connection()
    _send_command('AT+POP3DEL=' + number)

def pop_log_out():
    check_connection()
    _send_command('AT+POP3OUT')

##########################################################################$
# AT+CFUN=? set phone functionality (IE airplane mode on/off)
# AT+CMEE=1 error display related
# AT+CCLK="yy/MM/dd,hh:mm:ss+-zz" set clock
# AT+CIFSR get local IP address
#
# AT+CMMSINIT initialize MMS function
# AT+CMMSCURL="link" sets MMS center based on URL
###########################################################################
