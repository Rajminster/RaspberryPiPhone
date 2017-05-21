#!/usr/bin/python
# fona.py

from serial import Serial
from sys import exit
from time import sleep
import RPi.GPIO as gsm

class Fona():
    """Class to interact with FONA 2G GSM chip.

    Contains methods for powering GSM, checking if a successful connection can
    be established with the FONA device, sending commands (see README.md) to the
    device, checking the output of the device after commands, methods for basic
    commands such as checking FONA model and revision.

    Attributes:
        baud (int): baud rate for this device
        serialport (serial.Serial): serial port for communication between
        Raspberry Pi and FONA chip
        channel (int): pin number which FONA and GSM connect
    """

    baud = 9600
    serialport = Serial('/dev/ttyAMA0', baud, timeout=1)
    channel = 21

    @staticmethod
    def power_gsm():
        """Powers GSM connected to the pin whose value is in the channel variable.

        Raspberry Pi's built in GPIO library can be used to write logical HIGH and
        LOW to the channel the GSM is connected to in order to turn it on.
        """
        gsm.setwarnings(False)
        gsm.setmode(gsm.BCM)
        gsm.setup(channel, gsm.OUT)
        gsm.output(channel, gsm.HIGH)
        sleep(1)
        gsm.output(channel, gsm.LOW)

    @staticmethod
    def check_connection():
        """Checks if the FONA 2G GSM chip can be connected to successfully.

        If connecting is successful, this method outputs to the console that
        connection was SUCCESSFUL; otherwise, this method outputs to the console
        that connecting to the FONA device was UNSUCCESSFUL and raises an
        IOException.

        Raising the IOExecption would signal to whatever parent method that
        communcations between the Raspberry Pi and the FONA device are
        compromised.

        This method should be called before any of the below methods in a
        try-except block in order to ensure that the FONA chip is correctly
        connected. If an IOException is raised, handle in the parent method, not
        in this class.

        Raises:
            IOException if the Raspberry Pi cannot connect to the FONA device
        """
        """ AT command makes FONA output if connection was successful """
        send_command('AT\r')
        output = get_output()
        if 'OK' in output:
            print '\n\n***\n*** SUCCESSFUL connecting to FONA\n***\n\n'
        else:
            print '\n\n***\n*** UNSUCCESSFUL connecting to FONA\n***\n\n'
            raise IOException('Unable connecting to FONA 2G GSM')
    
    @staticmethod
    def send_command(data):
        """Send string command to serial port for the FONA device. See README.md
        for list of commands and their expected outputs. Serial ports must write
        data in the form of bytes, so unicode strings must be encoded. See:
            https://pythonhosted.org/pyserial/pyserial_api.html

        Arg:
            data (str): string command. NOTE: commands should end in '\r'.
        """
        serialport.write(data.encode('utf-8'))


    @staticmethod
    def get_output():
        """After sending command to the FONA device, this method obtains and
        returns its output for that command string.

        Returns:
            String of output from the FONA device
        """
        output = serialport.readlines()
        for i in range(len(output)):
            output[i] = output[i].rstrip()
        return output
    
    @staticmethod
    def get_model():
        """Send ATI command to output the FONA model and revision.

        First checks if there is a successful connection. If so, the command for
        outputting FONA model and revision is sent, and the output of the FONA
        is then returned; if a successful connection was not obtained, the
        method exits with EXIT_FAILURE.

        Returns:
            String of FONA model and revision
        """
        try:
            check_connection()
            send_command('ATI\r')
            return get_output()
        except IOException:
            print '\n\n***\n*** FONA Exception\n***\n\n'
            exit(1)

    @staticmethod
    def get_simcard_number():
        """Send AT+CCID command to output the SIM card number.

        First checks if there is a successful connection. If so, the command for
        outputting SIM card number is sent, and the output of the FONA
        is then returned; if a successful connection was not obtained, the
        method exits with EXIT_FAILURE.

        Returns:
            String of SIM card number
        """
        try:
            check_connection()
            send_command('AT+CCID\r')
            return get_output()
        except IOException:
            print '\n\n***\n*** FONA Exception\n***\n\n'
            exit(1)

    @staticmethod
    def close():
        """Close the serial port."""
        serialport.close()
