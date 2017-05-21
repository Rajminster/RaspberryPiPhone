#!/usr/bin/python
# call_thread.py

from threading import Thread
import fona
import RPi.GPIO as gsm

class Call_Thread(Thread):
    """Thread to continually poll the GSM if a call was received.

    Whenever the GSM's input pin outputs a logical HIGH, then either a message
    or call has been received. In order to determine which has been received,
    the number of messages received before checking is compared with the current
    number of messages received. If this new value is equal, then a call has
    been receieved, and a file accessible to the UI thread is written to which
    signals an incoming call.

    Attributes:
        sms_received (int): number of SMSs ever received (used to determine if a
        call or message was received). Value must be saved to a file
        file (File): file where the number of SMS messages received is saved
        signal (File): file where this thread signals if a call is incoming
    """
    def __init__(self, sLock, delay=2):
        """Constructor for Call_Thread object which inherits from
        threading.Thread.
        
        Args:
            sLock (threading.Lock): lock in order to write commands to the FONA
            from this thread and the SMS thread
            delay (int): amount of time to pass between checks (default is 2
            seconds)
        """
        Thread.__init__(self)
        self.file = open('sms_received.txt', 'w+')
        self.signal = open('/../phone/signal.txt', 'w+')
        self.signal.write('False')
        try:
            self.sms_received = int(self.file.readline())
        except ValueError:
            """ empty file """
            self.sms_received = 0
            self.file.write(str(self.sms_received))
        self.sLock = sLock
        self.delay = delay

    def run(self):
        """Method to continually poll if the GSM received any calls.

        Every 'delay' seconds, this method checks the GSM for if a new call has
        been received. A new call is received whenever the GSM's input pin
        outputs a logical HIGH and when the number of messages received before
        the check and after the check are the same. Once a call is received,
        the UI thread is signalled through one of its thread conditional
        variables.
        """
        while True:
            try:
                self.sLock.acquire()
                fona.check_connection()
                # if logical HIGH received then a call or message was received
                if gsm.input(INPUT_PIN):
                    # get number of SMSs
                    fona.send_command('AT+CPMS?\r')
                    num = int(fona.get_output()[1].split(',')[1])
                    """ determine if a call was received (num would equal sms_received) """
                    if num == self.sms_received:
                        self.signal.write('True')
                    elif num > self.sms_received:
                        self.sms_received = num
                        self.file.write(str(self.sms_received)) # overwrite old value
            except:
                print '***\n*** Error communicating with FONA\n***'
                ###################### TODO handle/signal UI thread ######################
                #### either handle here or throw exception up ####
            finally:
                self.sLock.release()
            sleep(self.delay)
