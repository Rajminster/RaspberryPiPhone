#!/usr/bin/env python

from threading import Thread
from time import sleep

from fona_commands import sms_received

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class SMS_Thread(Thread):
    """Thread to continually poll the FONA device if an SMS was received.

    Whenever the fona_commands method message_received returns a number greater
    than 0, new messages have arrived to the FONA. The signal thread is
    notified of a new message by writing to the file sms_signal.txt in the
    message application directory. Either True or False exists in this file so
    that if a message has been received and in the time it takes to check
    sms_signal.txt a new message is received, the signal thread does not need to
    worry about the number of new messages received but rather the fact that
    there are new messages.

    Once the signal thread has finished acknowledging the new messages, it will
    also write to the sms_signal.txt file. It will write False to signal to
    itself that no new messages have arrived.

    Since two threads will be writing to the same resource, a lock is needed for
    writing to sms_signal.txt. Since the SMS thread calls methods in
    fona_commands, it will be writing to the FONA device serial port.
    Concurrently, the signal thread will most likely be writing to the FONA
    various commands as a part of regular operation. Because of this, another
    threading lock is required to maintain the shared FONA port resource.
    """

    def __init__(self, fona_lock, sms_lock, delay=5):
        """Constructor for SMS_Thread object.

        Class which inherits from threading.Thread. Constructor to setup class
        variables and open sms_signal.txt file for communication between the
        SMS_Thread and the Signal_Thread classes.
       
        Args:
            fona_lock (threading.Lock): lock in order to write commands to the
            FONA port from this thread, the call thread, and the main thread
            sms_lock (threading.Lock): lock in order to write to the
            sms_signal.txt file from SMS_Thread and Signal_Thread
            delay (float): amount of time to pass between checks (default is 5
            seconds)
        """
        Thread.__init__(self)
        self.sms_signal = open('sms_signal.txt', 'w+')
        self.fona_lock = fona_lock
        self.sms_lock = sms_lock
        self.delay = delay

    def run(self):
        """Continually poll the FONA device to see if any new messages have been
        received.

        Method which overrides the method run from threading.Thread. Called
        whenever the method start is called on an instance of SMS_Thread. 

        Using the fona_commands.message_received method, run checks to see if
        message_received outputs a number greater than zero. The output of
        message_rceeived is the number of new messages received (new in the
        sense that the main thread has not accounted for these messages). This
        method runs as soon as the Raspberry Pi is powered on, and it will run
        for as long as it is on.

        Every 'delay' seconds, the output of fona_commands.message_received is
        checked for greater than zero. If the number of messages received is
        greater than zero, then new messages have been received by the FONA;
        this method signals the signal thread of the presence of these new
        messages by writing to the sms_signal.txt file the string True.

        If the signal thread reads the sms_signal.txt file for the messages
        application, it will see that it contains True if new messages have been
        received. If this is the case, then the signal thread should perform any
        necessary tasks for notifying the OS UI to update any type of display to
        inform the user of an incoming SMS. Once this process is done, the
        signal thread should then acquire the threading lock for the
        sms_signal.txt file and write the string False so that whenever it
        checks the sms_signal.txt file again, it will be accurate.
        """
        while True:
            self.fona_lock.acquire()
            if sms_received() > 0:
                print '\n***\n*** SMS RECEIVED\n***'
                self.sms_lock.acquire()
                self.sms_signal.write('True')
                self.sms_signal.seek(0)
                self.sms_lock.release()
            print '***\n*** Error communicating with FONA\n***'
            self.fona_lock.release()
            sleep(self.delay)
