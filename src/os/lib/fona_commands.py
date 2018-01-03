#!/usr/bin/env python3

from time import sleep

from fona import get_output, send_command, send_eot

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-28'
__version__ = '1.0'

"""General Purpose Library for 2G FONA Device.

Using methods defined in the fona.py file, this library defines useful
functions which utilize these fona methods as building blocks to
accomplish more complex tasks such as answer a call, send an email, or
connect to another device using the TCP protocol.

Using the 2G FONA UFL GSM US Edition SIM800 Series device, this library
defines methods in the following order:
    Diagnostic Information
    Time & Location
    Phone Functionality
    Short Message Service
    Audio
    Email
    Networking

Describe what these methods look like.
"""

MIMNUM = 0
FULL = 1
DISABLE = 4

########################################################################
#                       DIAGNOSTIC INFORMATION                         #
########################################################################
def get_model():
    """Send ATI command to output the FONA identification information.

    This method first checks if there is a successful connection between
    the Raspberry Pi and the FONA device. If so, the command for
    outputting FONA identification information is sent, and the output
    of the FONA is then returned; if a successful connection was not
    obtained, the method raises the IOError to the caller.

    Returns:
        String of FONA model and revision
    """
    send_command('ATI')
    return get_output()

def get_simcard_number():
    """Send AT+CCID command to output the SIM card identifier (outputs
    Integrated Circuit Card ID (CCID)).

    The command for outputting SIM card number is sent, and the output
    of the FONA is then returned; if a successful connection was not
    obtained, the method raises the IOError to the caller.

    Returns:
        String of SIM card identifier
    """
    send_command('AT+CCID')
    return get_output()

def get_carrier_name():
    """Send AT+CSPN command to output the name of the carrier.

    First checks if there is a successful connection. If so, the command
    for outputting carrier name is sent, and the output of the FONA is
    then returned. If using a non-major carrier, it is possible for this
    method to return a string array which contains the string ERROR. If
    this is the case, this error string should be disregarded. If a
    successful connection was not obtained, the method raises the
    IOError to the caller.

    Returns:
        String of carrier name
    """
    send_command('AT+CSPN')
    return get_output()

def get_reception():
    """Send AT+CSQ command to output the reception of the FONA.

    First checks if there is a successful connection. If so, the command
    for outputting reception is sent, and the output of the FONA is then
    returned. The output of the FONA device after sending this command
    should be in the format:
        ['AT+CSQ', '+CSQ: X,0', '', 'OK']
    where the X determines the strength of the reception: a higher
    number means a stronger reception. If a successful connection was
    not obtained, the method raises the IOError to the caller.

    Returns:
        String of reception
    """
    send_command('AT+CSQ')
    return get_output()[1].split(',')[0].split(' ')[1]


def get_battery_percentage():
    """Send AT+CBC command to output the battery percentage of the FONA
    device.

    First this method checks the connection from the FONA device to the
    Raspberry Pi. Then this device sends the command to output the
    battery percentage of the FONA device which is then returned as a
    string array.

    Returns:
        Battery percentage of the FONA device in a string array in the
        form:
            ['AT+CBC', '+CBC: 0,100,4220', '', 'OK']
        where the percentage is the number between the 0 and 4220 (in
        this case, the FONA device is 100% charged)
    """
    send_command('AT+CBC')
    return get_output()

def echo_on():
    send_command('ATE1')
    get_output()

def echo_off():
    send_command('ATE0')
    get_output()

def factory_reset():
    send_command('AT&F0')
    get_output()

def power_off():
    send_command('AT+CPOWD=1')
    get_output()

########################################################################
#                          TIME & LOCATION                             #
########################################################################
def get_local_timestamp():
    """
    """
    send_command('AT+CLTS?')
    return get_output()

def get_time():
    """
    """
    send_command('AT+CIPGSMLOC=1,1')
    return get_output()

def gsm_location():
    send_command('AT+CIPGSMLOC=1')
    return get_output()

def get_lat_long():
    """
    """
    send_command('AT+CIPGSMLOC=1,1')
    return get_output()

def get_time():
    send_command('AT+CCLK?')
    return get_output()[1]

def set_time(time):
    """Time is in format yy/MM/dd,hh:mm:ss+-zz."""
    send_command('AT+CCLK="%s"' % time)
    get_output() # TODO: possibly do error checking on output or have method that does that

########################################################################
#                         PHONE FUNCTIONALITY                          #
########################################################################
def get_phone_status():
    """Output the status of the phone activity.

    To output the status, this method first checks the connection
    between the Raspberry Pi and the FONA device. If there exists a
    secure connection, then this method will send the command AT+CPAS
    which makes the FONA device output the status of the phone.
    Depending on the output of this method, it can be determined if
    there is an incoming call to the FONA, no calls, or a call in
    process.

    After writing the AT+CPAS command to the FONA device, its output is
    in the format:
        ['AT+CPAS', '+CPAS: 0', '', 'OK']
    So the second element of the string array, second element on the
    split of whitespace is returned. If this value is a 0, then this
    means there are no calls occurring or incoming. 2 means the status
    is unknown. 3 means there is an incoming call, 4 means there is a
    call in progress.

    Returns:
        String of the current status of phone activity. Values can only
        be 0, 2, 3, or 4
    """
    send_command('AT+CPAS')
    return get_output()[1].split(' ')[1]

def set_phone_functionality(func):
    """Sets phone functionality.

    MINIMUM = 0: the smallest amount of functionality
    FULL    = 1: full phone functionality
    DISABLE = 4: disable phone transmission and receive
    """
    if func != MIMNUM or func != FULL or func != DISABLE:
        raise ValueError('Invalid value for functionality')
    send_command('AT+CFUN=%s' % func)

def call_number(number):
    """Call the phone number parameter.

    First check for a successful connection between the FONA device and
    the Raspberry Pi. If this check is successful, then send the command
    for calling a phone number.

    Arg:
        number (str): string of the phone number to call. NOTE: this
        phone number should contain an international code
    """
    send_command('ATD%s;' % number)
    get_output()

def answer_call():
    """Answer incoming call to this FONA device.

    If a call is incoming, this method will send the ATA command which
    instructs the FONA device to answer that call.
    """
    send_command('ATA')
    get_output()

def end_call():
    """Ends any current call in process.

    Ends call in process by sending the ATH command. Since this method
    should be called whenever a call is in process, this method does not
    check for successful connection with the FONA device."""
    send_command('ATH')
    get_output()

def mute_call():
    """Mutes any call in process.

    Turns on muting for the current call in process. This method will
    only mute a call if a call is in process.
    """
    send_command('AT+CMUT=1')
    get_output()

def unmute_call():
    """Turns off mute setting for a current call in process.

    This method will only turn off the mute setting for a call that is
    in process and will not do anything otherwise.
    """
    send_command('AT+CMUT=0')
    get_output()

def set_ringtone_volume(volume):
    if volume < 0 or volume > 100:
        raise ValueError('Out of range value for volume')
    send_command('AT+CRSL=%d' % volume)
    get_output()

def open_microphone():
    send_command('AT+CEXTERN=0')
    get_output()

def close_microphone():
    send_command('AT+CEXTERN=1')
    get_output()

def enable_caller_id():
    send_command('AT+CLIP=1')
    get_output()

def disable_caller_id():
    send_command('AT+CLIP=0')
    get_output()

########################################################################
#                       SHORT MESSAGE SERVICE                          #
########################################################################
def send_sms(number, message):
    """Send an SMS to the phone number which is given by the string
    parameter number.

    To send an SMS, first the connection with the FONA is checked. If
    successful, the AT command for changing the message type (AT+CMGF)
    is written to the FONA device. When entering this command in the
    FONA terminal, this allows the text directly typed in the terminal
    to be used as the SMS to be sent. The command for setting the phone
    number to be texted is written, using the number parameter, followed
    by writing the message to the FONA device; this is why changing the
    text type was required. Finally the CTRL-Z signal is sent, escaping
    the direct message entry and sending the message to the desired
    recipient.

    Args:
        number (str): string of the phone number to send the message to.
        NOTE: the number which is the intended recipient must have the
        appropriate international code
        message (str): the message part of the SMS to be sent to the
        phone number
    """
    send_command('AT+CMGF=1')
    send_command('AT+CMGS="%s"' % number)
    send_command(message)
    send_eot()
    get_output()

def sms_received():
    """Determines if any new SMSs have been sent to the FONA device.

    To determine if any new SMS has been received, this method first
    checks FONA connection. If successful, it writes to the FONA serial
    port the AT command which outputs the number of total SMSs received.
    The get_output method will return a string array whose second index
    contains the number of received SMSs.

    This value is the total number of SMSs received, according to the
    FONA device; however, it is not the total number of SMSs accounted
    for (or recorded). To save the number of SMSs accounted for
    (non-new), we save the current value of SMSs received to a file (if
    it's greater than the number of recorded SMSs). Initially, this file
    will be empty, so the value for this variable is assumed to be zero.

    At any point in calling this method, the number of SMSs received
    will always be greater than or equal to the number of SMSs recorded.
    If the number of SMSs received by the FONA is greater than the
    number of SMSs recorded, then new SMSs have been received. This is
    why the max of number of SMSs received and number recorded is the
    new value for number of SMSs recorded.

    This method returns the difference between number of SMSs received
    by the FONA and number of SMSs recorded. If no new SMSs have been
    received, the number of SMSs received and the number of SMSs
    recorded will be equal, meaning this method will return zero to
    indicate no new SMSs; otherwise this method will return the number
    of new SMSs.

    Returns:
        If any new SMSs have been received, this method returns non zero
        (the number of new SMSs unaccounted for); otherwise it returns
        zero
    """
    send_command('AT+CPMS?')
    sms_received = int(get_output()[1].split(',')[1])
    f = open('sms_record.txt', 'r')
    try:
        sms_recorded = int(f.readline())
    except ValueError:
        """empty file"""
        sms_recorded = 0
    with open('sms_record.txt', 'w+') as record:
        record.write(str(max(sms_received, sms_recorded)))
    return sms_received - sms_recorded

def _parse_message(output):
    """Parses the message payload from the FONA device output after
    sending it its command for outputting the full details of an SMS
    received.

    In order to tell when the message begins, this method must begin
    iterating over the output parameter given. Since any number of
    commands at least one could have been written to the FONA before
    this method has been called, the only way to determine where the
    message begins is the iterate until the string denoting message
    status type (string beginning with +CMGR:) is found; the next string
    is the beginning of the message.

    The output parameter could have the format:
        [AT+CMGR=2', '+CMGR: "REC READ", "+XXXXXXXXXXX","","17/05/28,
        14:33:14-16",145,4,0,0,"+12063130055", 145,5', 'Hello', '',
        'OK']
    where elements are indicated by single quotes and the X's make up
    the phone number of the sender. Here, the SMS begins in the second
    array entry and ends at the third to last, with empty entries
    indicating a new line within the message. The OK string is a signal
    from the FONA device that the command has successfully finished.

    Arg:
        output (str list): string array outputted from the FONA device
        serial port and given by the get_output method

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
    """Returns array of number, timestamp, message tuples for all SMSs
    received by the FONA device with successful connection to Raspberry
    Pi.

    In order to get any SMS received with useful metadata, first two
    commands must be sent to the FONA device: AT+CMGF=1 which sets SMS
    message format to text and AT+CSDH=1 which shows SMS text mode
    metadata (timestamp received, sender phone number, message contents,
    etc.).

    With this setup, the AT+CPMS command is sent which outputs the total
    number of SMSs received which is used to iterate through each SMS
    received. To output metadata about the ith SMS received, the
    AT+CMGR=i command is sent, and with the first two commands sent, the
    FONA device outputs clear metadata about the ith SMS which is
    appended to the tuple array to be returned.

    In this method, the total number of SMSs received is indexed as the
    fifth element of the get_output string array because before the
    AT+CPMS? command was entered, two other commands were entered which
    each take two indices in the array. NOTE: the FONA device does not
    use zero-indexing when outputting SMSs received.

    Returns:
        Array of sender phone number, SMS timestamp, and message tuples
        of all SMSs received by the FONA device
    """
    send_command('AT+CMGF=1')
    send_command('AT+CSDH=1')
    send_command('AT+CPMS?')
    sms_received = int(get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, sms_received + 1):
        send_command('AT+CMGR=' + str(i))
        output = get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_new_sms():
    """Returns array of number, timestamp, message tuples for all SMSs
    which have been recently received by the FONA which have just been
    accounted for in the sms_received method.

    This method first calls the sms_received method which ensures a
    successful connection exists between the FONA device and the
    Raspberry Pi as well as find out how many SMSs have been marked as
    'new'. After this, the method writes the AT+CMGF=1 command to set
    the SMS message format to text to make message output legible. Next
    it writes the AT+CSDH=1 command which makes the FONA console output
    more detailed metadata about SMSs received.

    The command to output the total number of SMSs received is then
    entered to only grab the newest received to return. This value is
    obtained by indexing into the fifth element of the get_output
    string array because it's the output of the third command entered;
    since each command requires two indices of the get_output array (one
    for the command and one for its output), it's the sixth place (5
    when zero-indexed).

    Now the method iterates through the new SMSs received and appends
    those to the array to be returned with metadata phone number of
    sender, timestamp of message, and message contents. NOTE: the FONA
    does not zero-index SMSs received, so 1 is added to the lower and
    upper bound of the for loop.

    Returns:
        Array of sender phone number, message timestamp, and message
        contents tuples for new SMSs received
    """
    new_received = message_received()
    send_command('AT+CMGF=1')
    send_command('AT+CSDH=1')
    send_command('AT+CPMS?')
    sms_received = int(get_output()[5].split(',')[1])
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - new_received + 1, sms_received + 1):
        send_command('AT+CMGR=' + str(i))
        output = get_output()
        messages['number'].append(output[1].split('"')[3].replace('+', ''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_newest_sms(n):
    """Returns array of sender phone number, timestamp, and message
    content tuples of the n newest received SMSs.

    This is accomplished by first checking for an existing connection
    between the Raspberry Pi and the FONA device. This method then
    writes the AT+CPMS? command to output the total number of SMSs
    received in order to error check the n argument. After this,
    commands for setting SMS message format and output detailed SMS
    metadata are entered (AT+CMGF=1 and AT+CSDH=1, respectively).
    Because the output from these two commands are not necessary, this
    method calls the get_output method in order to flush the FONA
    serial port's output.

    Now the method iterates through the n newest SMSs and appends their
    sender phone number, message timestamp, and message contents to the
    array it will return. NOTE: the FONA does not zero-index SMSs
    received, so 1 is added to the lower and upper bounds of the for
    loop.

    Arg:
        n (int): the number of newest SMSs to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the
        number of SMSs received

    Returns:
        Array of sender phone number, message timestamp, and message
        contents tuples for newest SMSs received
    """
    send_command('AT+CPMS?')
    sms_received = int(get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    send_command('AT+CMGF=1')
    send_command('AT+CSDH=1')
    get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(sms_received - n + 1, sms_received + 1):
        send_command('AT+CMGR=' + str(i))
        output = get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

def get_n_oldest_sms(n):
    """Returns array of sender phone number, timestamp, and message
    content tuples of the n oldest received SMSs.

    This is accomplished by first checking for an existing connection
    between the Raspberry Pi and the FONA device. This method then
    writes the AT+CPMS? command to output the total number of SMSs
    received in order to error check the n argument. After this,
    commands for setting SMS message format and output detailed SMS
    metadata are entered (AT+CMGF=1 and AT+CSDH=1, respectively).
    Because the output from these two commands are not necessary, this
    method calls the get_output method in order to flush the FONA serial
    port's output.

    Now the method iterates through the n oldest SMSs and appends their
    sender phone number, message timestamp, and message contents to the
    array it will return. NOTE: the FONA does not zero-index SMSs
    received, so 1 is added to the lower and upper bounds of the for
    loop.

    Arg:
        n (int): the number of oldest SMSs to return

    Raises:
        ValueError if the value for n is less than 1 or greater than the
        number of SMSs received

    Returns:
        Array of sender phone number, message timestamp, and message
        contents tuples for oldest SMSs received
    """
    send_command('AT+CPMS?')
    sms_received = int(get_output()[1].split(',')[1])
    if n > sms_received or n < 1:
        raise ValueError('\n***\n*** Out of range value for n\n***\n')
    send_command('AT+CMGF=1')
    send_command('AT+CSDH=1')
    get_output()
    messages = {'number':[], 'timestamp': [], 'message': []}
    for i in range(1, n + 1):
        send_command('AT+CMGR=' + str(i))
        output = get_output()
        messages['number'].append(output[1].split('"')[3].replace('+',''))
        messages['timestamp'].append(output[1].split('"')[7])
        messages['message'].append(_parse_message(output))
    return messages

########################################################################
#                                AUDIO                                 #
########################################################################
def start_audio(file_path):
    """TODO: instead of 50 default volume, save volume to a file"""
    """Use the FONA device to begin playing an audio file, given its
    file path.

    In order to play an audio file with the FONA device, a call cannot
    be in progress. If this is the case, the command AT+CMEDPLAY=1 along
    with the file path for the device, channel, and volume is written to
    the FONA device. The audio file may be in the WAV, PCM, AMR, or MP3
    format.

    For the channel parameter, this method passes 0 for the main
    channel; 1 would be used for an aux channel.

    This method's intended purpose is to play voicemail files.

    Arg:
        file_path (str): location of the audio file to be played
    """
    send_command('AT+CMEDPLAY=1,%s,0,50' % file_path)
    get_output()

def stop_audio(file_path):
    """Stop playing any audio file currently playing.

    This method writes to the FONA device serial port the command for
    stopping the audio file located at the given file path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    send_command('AT+CMEDPLAY=0,%s,0,50' % file_path)
    get_output()

def pause_audio(file_path):
    """Pause a playing audio file currently playing.

    This method writes to the FONA device serial port the command for
    only pausing a playing audio file located at the given file path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    send_command('AT+CMEDPLAY=2,%s,0,50' % file_path)
    get_output()

def play_audio(file_path):
    """Continue playing an audio file wherever it has been left off.

    This method only writes to the FONA device port the command to
    continue playing whichever audio file is saved at the given file
    path.

    The audio file may be in the WAV, PCM, AMR, or MP3 format.

    Arg:
        file_path (str): location of the audio file to be played
    """
    send_command('AT+CMEDPLAY=3,%s,0,50' % file_path)
    get_output()

def set_audio_file_volume(volume):
    """Sets the volume for playing an audio file only.

    To set the volume used whenever an audio file is being played, this
    method writes to the FONA port the command.

    Arg:
        volume (int): the volume level to be set (must be between 0 and
        100 inclusive)

    Raises:
        ValueError if the value for volume is less than 0 or greater
        than 100
    """
    if volume < 0 or volume > 100:
        raise ValueError('Out of range value for volume')
    send_command('AT+CMEDIAVOL=%d' % volume)
    get_output()

def start_voice_recording():
    """
    """
    # format: AT+CREC=1, file_path, 1 (for WAV format), 0 (use int value for how long you want the recording to be), 0 (for FAT format), 3 (highest quality), 0 (MIC1)
    send_command('AT+CREC=1')

def set_speaker_volume(volume):
    """Set volume for Raspberry Pi speakers.

    Unlike the set_audio_file_volume method, this method sets the volume
    for the entire phone's speakers. To do so, this method writes the
    ATL command with the given volume parameter to the FONA device.

    Arg:
        volume (int): volume of the speakers to be set

    Raises:
        ValueError if the value for volume is less than 0 or greater
        than 9
    """
    if volume < 0 or volume > 9:
        raise ValueError('\n***\n*** Out of range value for volume\n***')
    send_command('ATL%d' % volume)
    get_output()

########################################################################
#                                EMAIL                                 #
########################################################################
def set_sender_address(address, name):
    send_command('AT+SMTPFROM=%s,%s' % (address, name))
    get_output()

def set_recipient_address(address, name):
    send_command('AT+SMTPRCPT=%s,%s' % (address, name))
    get_output()

def set_email_subject(subject):
    send_command('AT+SMTPSUB=%s' % subject)
    get_output()

def set_email_body(body):
    send_command('AT+SMTPBODY=%s' % str(len(body)))
    send_command(body)
    get_output()

def email_txt_file(file_name, length):
    # NOTE: length is the maximum length of a TXT file name
    send_command('AT+SMTPFILE=1,' + file_name + ',' + length + ',0')
    get_output()

def send_email():
    send_command('AT+SMTPSEND')
    get_output()

def set_pop3_server_account(server, user, password):
    send_command('AT+POP3SRV=' + server + ',' + user + ',' + password)
    get_output()

def pop_log_in():
    send_command('AT+POP3IN')
    get_output()

def get_email_num_size():
    send_command('AT+POP3NUM')
    get_output()

def get_email_size(number):
    send_command('AT+POP3LIST=' + number)
    get_output()

def set_delete_email(number):
    send_command('AT+POP3DEL=' + number)
    get_output()

def pop_log_out():
    send_command('AT+POP3OUT')
    get_output()

########################################################################
#                              NETWORKING                              #
########################################################################
def initiate_tcp_connection(ip_address):
    send_command('AT+CIPSTART=2')
    get_output()

def send_through_tcp(ip_address):
    send_command('AT+CIPSEND=2')
    get_output()

def close_connection():
    send_command('AT+CIPCLOSE=0')
    get_output()

def get_local_ip():
    send_command('AT+CIFSR')
    get_output()

def pin_required():
    """Check to see if the PIN is required to be entered."""
    send_command('AT+CPIN?')
    return get_output()[1].split(':')[1]

def network_registration():
    send_command('AT+CREG?')
    return get_output()
