#!/usr/bin/env python
# fona.py

from serial import Serial
from sys import exit
from time import sleep
from traceback import format_exc

__author__ = "Nikola Istvanic"
__date__ = "2017-05-24"
__version__ = "1.0"

class Fona():
    """Class to interact with FONA 2G device.
    
    Contains methods for interacting with the FONA device: checking if a successful
    connection can be established with the FONA device, sending commands (see README.md)
    to the device, checking the output of the device after commands, methods for basic
    commands such as checking FONA model and revision.

    Attributes:
        baud (int): baud rate for FONA device
        fona_port (serial.Serial): serial port for communication between Raspberry Pi
        and FONA device
    """

    baud = 9600
    fona_port = Serial('/dev/ttyUSB0', baud, timeout=1)

    @staticmethod
    def check_connection():
        """Checks if the FONA 2G device can be connected to successfully.

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
            IOError if the Raspberry Pi cannot connect to the FONA device
        """
        """AT command makes FONA output if connection was successful"""
        Fona.send_command('AT')
        output = Fona.get_output()
        if 'OK' in output:
            print '\n\n***\n*** SUCCESSFUL connecting to FONA\n***\n\n'
        else:
            print '\n\n***\n*** UNSUCCESSFUL connecting to FONA\n***\n\n'
            raise IOError('\n\n***\n*** Unable connecting to FONA 2G device\n***')
    
    @staticmethod
    def send_command(data):
        """Send string command to serial port for the FONA device. See README.md
        for list of commands and their expected outputs. Serial ports must write
        data in the form of bytes, so unicode strings must be encoded. See:
            https://pythonhosted.org/pyserial/pyserial_api.html

        Arg:
            data (str): string command. NOTE: \r is appended to commands
        """
        data += '\r'
        Fona.fona_port.write(data.encode('utf-8'))

    @staticmethod
    def get_output():
        """After sending command to the FONA device, this method obtains and
        returns its output for that command string.

        Returns:
            String of output from the FONA device
        """
        output = Fona.fona_port.readlines()
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
            Fona.check_connection()
            Fona.send_command('ATI')
            return Fona.get_output()
        except IOError:
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
            Fona.check_connection()
            Fona.send_command('AT+CCID')
            return Fona.get_output()
        except IOError:
            print '\n\n***\n*** FONA Exception\n***\n\n'
            exit(1)
    
    @staticmethod
    def get_reception():
        """Send AT+CSQ command to output the reception of the FONA

        First checks if there is a successful connection. If so, the command for
        outputting reception is sent, and the output of the FONA is then returned;
        if a successful connection was not obtained, the method exits with
        EXIT_FAILURE.

        Returns:
            String of reception
        """
        try:
            Fona.check_connection()
            sleep(1)
            Fona.send_command('AT+CSQ')
            return Fona.get_output()
        except IOError:
            print '\n\n***\n*** FONA Error\n***\n\n'
            exit(1)
        
    @staticmethod
    def get_carrier_name():
        """Send AT+CSPN command to output the name of the carrier

        First checks if there is a successful connection. If so, the command for
        outputting carrier name is sent, and the output of the FONA is then returned;
        if a successful connection was not obtained, the method exits with
        EXIT_FAILURE. If there is no carrier, this method returns 'ERROR' string.

        Returns:
            String of carrier name
        """
        try:
            Fona.check_connection()
            sleep(1)
            Fona.send_command('AT+CSPN')
            output = Fona.get_output()
            """
            if 'ERROR' in output:
                raise NoCarrierException('\n\n***\n*** No carrier detected by FONA device\n***')
            """
            return output
        except IOError:
            print '\n\n***\n*** FONA Error\n***\n\n'
            exit(1)

    @staticmethod
    def close():
        """Close the serial port."""
        Fona.fona_port.close()
