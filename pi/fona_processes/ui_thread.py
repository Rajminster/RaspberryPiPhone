#!/usr/bin/env python

from threading import Thread

__author__ = 'Nikola Istvanic'
__date__ = '2017-06-05'
__version__ = '1.0'

class UI_Thread(Thread):
    def __init__(self, fona_lock, call_lock, sms_lock):
        self.fona_lock = fona_lock
        self.call_lock = call_lock
        self.sms_lock= sms_lock

    def _call_incoming(self):
        return open('../phone/call_signal.txt', 'r').readline() == 'True'

    def _update_call_file(self):
        file = open('../phone/call_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def handle_call(self):
        if _call_incoming():
            _update_call_file()
            # handle changing GUI to handle an incoming call
            # is file.close() required or will it break things?

    def _sms_incoming(self):
        return open('../message/sms_signal.txt', 'r').readline() == 'True'

    def _update_sms_file(self):
        file = open('../message/sms_signal.txt', 'w+')
        self.call_lock.acquire()
        file.write('False')
        self.call_lock.release()
        file.close()

    def handle_sms(self):
        if _sms_incoming():
            _update_sms_file()
            # handle changing GUI to handle an incoming sms
