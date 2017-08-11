#!/usr/bin/env python

from threading import Thread
from time import sleep

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class Main_Thread(Thread):
    """Thread class to create and display the UI of the Raspberry Pi Phone.

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

    From this thread, all of the UI elements are created and loaded. In this
    file there are methdos which create initial elements of the UI, but it also
    contains that load other elements defined elsewhere. For example, when
    booting, this class will load only the initial graphics for starting up, but
    after that it will load and hand over control to the homescreen UI element
    which will dictate the appearance of the screen.
    """

    def __init__(self, fona_lock, call_lock, sms_lock, delay=5):
        """Constructor for Main_Thread object.

        Args:
            fona_lock (threading.Lock): lock used to make sure only one of the
            thread classes defined in fona_processes directory writes to the
            FONA serial port at a time
            call_lock (threading.Lock): lock used to make sure only one of
            either Main_Thread or Call_Thread writes to the call_signal.txt file
            sms_lock (threading.Lock): lock used to make sure only one of either
            Main_Thread or SMS_Thread writes to the sms_signal.txt file
            delay (float): amount of time to delay between checking the
            call_signal.txt and sms_signal.txt files (default is 5)
        """
        Thread.__init__(self)
        self.fona_lock = fona_lock
        self.call_lock = call_lock
        self.sms_lock = sms_lock
        self.delay = delay
        #################### TODO ####################
        # self.display_boot_screen()
        # self.load_homescreen()
        ##############################################

    def display_boot_screen(self):
        """Display the boot loading screen while setting up hardware/software."""
        pass

    def load_homescreen(self):
        """Load/display UI for homescreen as well as load the controller for that UI."""
        pass

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
        return open('call_signal.txt', 'r').readline() == 'True'

    def _update_call_file(self):
        """Helper method to write to the call_signal.txt file False from this
        thread to indicate the incoming call is going to be tended to.

        This method first opens the call_signal.txt to write the string False to
        it. It then will block until it acquires the call_lock which it shares
        with the Call_Thread object. The line is written, the lock is released,
        and the file is closed. After this method, the UI should be altered as a
        result of this incoming call.
        """
        file = open('call_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def check_call(self):
        """Uses the _check_call_signal method to see if the Call_Thread has
        detected any incoming phone call.

        If the call_signal.txt file contains True, the file will be updated to
        contain False, and UI elements should be updated to tell the user of the
        incoming call. Otherwise, nothing will happen.
        """
        if self._check_call_signal():
            self._update_call_file()
            #################### TODO ####################
            # handle changing GUI to handle an incoming call
            ##############################################

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
        and the file is closed. After this method, the UI should be altered as a
        result of incoming SMSs.
        """
        file = open('sms_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def check_sms(self):
        """Uses the _check_sms_signal method to see if the SMS_Thread has
        detected any incoming SMSs.

        If the sms_signal.txt file contains True, the file will be updated to
        contain False, and UI elements should be updated to tell the user of the
        new SMSs. Otherwise, nothing will happen.
        """
        if self._check_sms_signal():
            self._update_sms_file()
            #################### TODO ####################
            # handle changing GUI to handle an incoming call
            ##############################################

    def run(self):
        """Method which dictates what this thread does when it is created.

        Continually check the call_signal.txt and sms_signal.txt files which are
        modified in the Call_Thread and SMS_Thread classes, respectively, as
        well as this class.

        The Call_Thread class will modify call_signal.txt by changing the file
        contents to be True if a call is incoming, and the Main_Thread will see
        this change and alter the file to contain False as well as update its
        user interface to reflect an incoming call.

        The SMS_Thread class will modify sms_signal.txt by changing the file
        contents to be True if any number of SMSs have been received by the FONA
        device. The Main_Thread class will notice this change and change the
        file contents back to be False and update its user interface to reflect
        this event.

        This process of checking the files is repeated as long as the device is
        powered on for every 'delay' seconds.
        """
        ################## TODO ##################
        # probably don't do this immediately when Pi is turned on; give it a second or two
        # have a way to stop this whenever the Pi is about to be turned off
        ##########################################
        while True:
            self.check_call()
            self.check_sms()
            sleep(self.delay)
