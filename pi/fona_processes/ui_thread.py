#!/usr/bin/env python

from threading import Thread

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class UI_Thread(Thread):
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

    def __init__(self, fona_lock, call_lock, sms_lock):
        """Constructor for UI_Thread object.

        Args:
            fona_lock (threading.Lock): lock used to make sure only one of the
            thread classes defined in fona_processes directory writes to the
            FONA serial port at a time
        """
        self.fona_lock = fona_lock
        self.call_lock = call_lock
        self.sms_lock = sms_lock

    def _call_incoming(self):
        """
        """
        return open('../phone/call_signal.txt', 'r').readline() == 'True'

    def _update_call_file(self):
        """
        """
        file = open('../phone/call_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def handle_call(self):
        """
        """
        if _call_incoming():
            _update_call_file()
            # handle changing GUI to handle an incoming call
            # is file.close() required or will it break things?

    def _sms_incoming(self):
        """
        """
        return open('../message/sms_signal.txt', 'r').readline() == 'True'

    def _update_sms_file(self):
        """
        """
        file = open('../message/sms_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def handle_sms(self):
        """
        """
        if _sms_incoming():
            _update_sms_file()
            # handle changing GUI to handle an incoming sms
