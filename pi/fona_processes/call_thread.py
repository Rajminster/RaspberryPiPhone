#!/usr/bin/env python

from fona_commands import check_connection, phone_status
from threading import Thread
from time import sleep

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class Call_Thread(Thread):
    """Thread to continually poll the FONA device for incoming phone calls.

    Whenever the RPi.GPIO.input method returns logical HIGH and the
    fona_commands method message_received returns 0, there is an incoming call
    to the FONA. The UI thread is signalled of this new call by writing to the
    file call_signal.txt in the call application directory. Either True or False
    exists in this file for the UI thread to check.

    Once the UI thread has finished acknowledging the incoming call, it will also
    write to the call_signal.txt file. It will write False to signal to itself
    that there are no incoming calls.

    Since two threads will be writing to the same resource, a lock is needed for
    writing to call_signal.txt. Since the call thread calls methods in
    fona_commands, it will be writing to the FONA device serial port.
    Concurrently, the UI thread will most likely be writing to the FONA various
    commands as a part of regular operation. Because of this, another threading
    lock is required to maintain the shared FONA port resource.

    Attribute:
        call_signal (File): file whose contents signals if an incoming call has
        been received. If there are messages which the UI has not yet
        acknowledged, this file should contain the string True; once the UI
        thread has finished acknowledging these new messages, it should write to
        this file False
    """

    def __init__(self, fona_lock, call_lock, delay=2):
        """Constructor for Call_Thread object.

        Class which inherits from threading.Thread. Constructor to setup class
        variables and open call_signal.txt file for communication between the
        Call_Thread and the UI_Thread classes.
       
        Args:
            fona_lock (threading.Lock): lock in order to write commands to the
            FONA port from this thread, the SMS thread, and the UI thread
            call_lock (threading.Lock): lock in order to write to the
            call_signal.txt file from Call_Thread and UI_Thread
            delay (int): amount of time to pass between checks (default is 2
            seconds)
        """
        Thread.__init__(self)
        self.call_signal = open('../phone/call_signal.txt', 'w+')
        self.fona_lock = fona_lock
        self.call_lock = call_lock
        self.delay = delay

    def run(self):
        """Continually poll the FONA device to see if there are any incoming
        calls.

        Method which overrides the method run from threading.Thread. Called
        whenever the method start is called on an instance of Call_Thread. 

        Using the RPi.GPIO.input and fona_commands.message_received methods, run
        checks to see if the Raspberry Pi's input GPIO pin outputs a logical
        HIGH and message_received outputs zero. If both of these are the case,
        then there is an incoming call to the FONA. This method runs as soon as
        the Raspberry Pi is powered on, and it will run for as long as it is on.

        Every 'delay' seconds, the output of RPi.GPIO.input and
        fona_commands.message_received are checked for logical HIGH and zero,
        respectively. If both of these occur, this method signals the UI thread
        that the FONA has an incoming call by writing to the call_signal.txt
        file the string True.

        If the UI thread reads the call_signal.txt file for the phone
        application, it will see that it contains True if there is an incoming
        call. If this is the case, then the UI thread should perform any
        necessary tasks for updating any type of display for signalling to the
        user of an incoming phone call. Once this process is done, the UI thread
        should then acquire the threading lock for the call_signal.txt file and
        write the string False so that whenever it checks the call_signal.txt
        file again, it will be accurate.
        """
        while True:
            try:
                self.fona_lock.acquire()
                check_connection()
                if phone_status() == '3':
                    self.call_lock.acquire()
                    self.call_signal.write('True')
                    self.call_lock.release()
            except:
                print '\n***\n*** Error communicating with FONA\n***'
                ################# TODO handle/signal UI thread #################
            finally:
                self.fona_lock.release()
            sleep(self.delay)
