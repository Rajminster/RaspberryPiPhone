#!/usr/bin/env python3

from call_thread import Call_Thread
from serial import SerialException
from sms_thread import SMS_Thread
from threading import Thread
from time import sleep

import logging
import os

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class Signal_Thread(Thread):
    """Thread class to run the Call_Thread and SMS_Thread simultaneously and
    inform the OS UI of any new calls or messages.

    Whenever the Raspberry Pi is booted, it needs two threads to continually
    poll the FONA device for calls and SMSs. Since both of these operations
    require writing commands to the FONA device, a lock for the FONA device is
    needed. Both of these threads also write to their own signal files. Because
    this thread also writes to those files, locks are needed for both files.

    Since this thread will also call methods defined in the fona_commands
    library, it will also need to write commands to the FONA device, so it
    should have a lock for the FONA.

    This class defines methods which act between the FONA device and elements of
    the UI: methods which check for output from the FONA to determine whether or
    not a call is incoming and then alter elements of the UI accordingly.

    From this thread signals to the UI are sent to notify it of new calls or
    messages.
    """

    def __init__(self, fona_lock, call_lock, sms_lock, delay=5):
        """Constructor for Signal_Thread object.

        Args:
            fona_lock (threading.Lock): lock used to make sure only one of the
            thread classes defined in fona_processes directory writes to the
            FONA serial port at a time
            call_lock (threading.Lock): lock used to make sure only one of
            either Signal_Thread or Call_Thread writes to the call_signal.txt
            file
            sms_lock (threading.Lock): lock used to make sure only one of either
            Signal_Thread or SMS_Thread writes to the sms_signal.txt file
            delay (float): amount of time to delay between checking the
            call_signal.txt and sms_signal.txt files (default is 5)
        """
        Thread.__init__(self)
        self.fona_lock = fona_lock
        self.call_lock = call_lock
        self.sms_lock = sms_lock
        self.sms_thread = SMS_Thread(self.fona_lock, self.sms_lock)
        self.call_thread = Call_Thread(self.fona_lock, self.call_thread)
        self.delay = delay
        logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(module)s::%(funcName)s: '
            '%(message)s', datefmt='%Y-%m-%d %H:%M:%S %Z')
        self.logger = logging.getLogger(__name__)

    def _check_call_signal(self):
        """Checks the call_signal.txt file to see if the Call_Thread background
        thread has detected an incoming call.

        The file call_signal.txt should only contain one line which is either
        True or False. If the line is True, then the Call_Thread has edited this
        file because there is an incoming call to the FONA device; otherwise,
        there is no incoming call to the FONA device.

        Returns:
            True if the first line of the call_signal.txt file contains True
            which indicates there is an incoming call; False otherwise to
            indicate that there is no incoming call
        """
        call_signal_file = open('.call_signal.txt', 'r')
        return open('.call_signal.txt', 'r').readline() == '1'

    def _update_call_file(self):
        """Helper method to write to the call_signal.txt file False from this
        thread to indicate the incoming call is going to be tended to.

        This method first opens the call_signal.txt to write the string False to
        it. It then will block until it acquires the call_lock which it shares
        with the Call_Thread object. The line is written, the lock is released,
        and the file is closed. After this method, the UI should be notified of
        this incoming call.
        """
        file = open('.call_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        file.close()
        self.call_lock.release()

    def check_call(self):
        """Uses the _check_call_signal method to see if the Call_Thread has
        detected any incoming phone call.

        If the call_signal.txt file contains True, the file will be updated to
        contain False, and UI should be notified to tell the user of the
        incoming call; otherwise, nothing will happen.
        """
        if self._check_call_signal():
            self._update_call_file()
            #################### TODO ##########################
            # handle signalling GUI to handle an incoming call #
            ####################################################

    def _check_sms_signal(self):
        """Checks the sms_signal.txt file to see if the SMS_Thread background
        thread has detected incoming SMSs.

        The file sms_signal.txt should only contain one line which is either
        True or False. If the line is True, then the SMS_Thread has edited this
        file because there is are incoming SMSs to the FONA device; otherwise,
        there are no SMSs received by the FONA device.

        Returns:
            True if the first line of the sms_signal.txt file contains True
            which indicates there are incoming SMSs; False otherwise to
            indicate that there are no incoming SMSs
        """
        return open('sms_signal.txt', 'r').readline() == 'True'

    def _update_sms_file(self):
        """Helper method to write to the sms_signal.txt file False from this
        thread to indicate the UI has acknowledged the incoming SMSs.

        This method first opens the sms_signal.txt to write the string False to
        it. It then will block until it acquires the sms_lock which it shares
        with the SMS_Thread object. The line is written, the lock is released,
        and the file is closed. After this method, the UI should be notified to
        alter as a result of incoming SMSs.
        """
        file = open('.sms_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        file.close()
        self.call_lock.release()

    def check_sms(self):
        """Uses the _check_sms_signal method to see if the SMS_Thread has
        detected any incoming SMSs.

        If the sms_signal.txt file contains True, the file will be updated to
        contain False, and UI elements should be updated to tell the user of the
        new SMSs. Otherwise, nothing will happen.
        """
        if self._check_sms_signal():
            self._update_sms_file()
            #################### TODO ##########################
            # handle signalling GUI to handle an incoming SMS  #
            # make sure this has a timer for how long it stays #
            ####################################################

    def run(self):
        """Method which will execute when this thread is started.

        Continually check the call_signal.txt and sms_signal.txt files which are
        modified in the Call_Thread and SMS_Thread classes, respectively, as
        well as this thread.

        The Call_Thread class will modify call_signal.txt by changing the file
        contents to be True if a call is incoming, and the Signal_Thread will
        see this change and alter the file to contain False as well as signal to
        the UI of this incoming call.

        The SMS_Thread class will modify sms_signal.txt by changing the file
        contents to be True if any number of SMSs have been received by the FONA
        device. The Signal_Thread class will notice this change and change the
        file contents back to be False and signal the UI of this incoming SMS.

        This process of checking the files is repeated as long as the device is
        powered on for every 'delay' seconds.

        Thread methods are called within a try-except block because whenever the
        FONA device is disconnected anyway to the Raspberry Pi, attempting to
        write to the port will result in a SerialException. This is handled in
        Signal_Thread because if the FONA is disconnected, this thread will be
        able to signal to the UI and OS.
        """
        ################## TODO ############################################################
        # probably don't do this immediately when Pi is turned on; give it a second or two #
        # have a way to stop this whenever the Pi is about to be turned off                #
        ####################################################################################
        self.call_lock.start()
        self.sms_lock.start()

        while True:
            try:
                self.check_call()
            except SerialException:
                self.fona_lock.release()
                #########################################################
                # TODO: handle loss of connection to FONA while running #
                #########################################################
            try:
                self.check_sms()
            except SerialException:
                self.fona_lock.release()
                #########################################################
                # TODO: handle loss of connection to FONA while running #
                #########################################################
            sleep(self.delay)
