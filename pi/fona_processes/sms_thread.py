#!/usr/bin/python
# sms_thread.py

from threading import Thread
import fona
import RPi.GPIO as gsm

class SMS_Thread(Thread):
    """Thread to continually poll the GSM if a message was received.

    Whenever the GSM's input pin outputs a logical HIGH, then either a message
    or call has been received. In order to determine which has been received,
    the number of messages received before checking is compared with the current
    number of messages received. If this new value is greater, then a new SMS
    has been receieved, and the UI thread is informed via file in the UI
    directory.

    Attributes:
        sms_received (int): number of SMSs ever received (used to determine if a
        call or message was received). Value must be saved to a file
        file (File): file where the number of SMS messages received is saved
        signal (File): file where this thread signals if a call is incoming
    """
    def __init__(self, sLock, delay=5):
        """Constructor for SMS_Thread object.
       
        Args:
            Lock (threading.Lock): lock in order to write commands to the FONA
            from this thread and the SMS thread
            delay (int): amount of time to pass between checks (default is 5
            seconds)
        """
        Thread.__init__(self)
        self.file = open('sms_received.txt', 'w+')
        self.signal = open('/../message/signal.txt', 'w+')
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
        """Method to continually poll if the GSM received any SMS messages.

        Every 'delay' seconds, this method checks the GSM for if a new message
        has been received. A new message has been received whenever the GSM's
        input pin outputs a logical HIGH and when the number of messages
        received before the check is less than the number after the check. Once
        a message is received, the UI thread is signalled through local file.
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
                    """ determine if a call was received (num would greater than sms_received) """
                    if num > self.sms_received:
                        self.sms_received = num
                        self.file.write(str(self.sms_received)) # overwrite old value
                        self.signal.write('True')
            except:
                print '***\n*** Error communicating with FONA\n***'
                ###################### TODO handle/signal UI thread ######################
            finally:
                self.sLock.release()
            sleep(self.delay)
