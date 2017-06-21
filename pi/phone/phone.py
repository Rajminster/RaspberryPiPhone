#!/usr/bin/python
# ui_thread.py

class UI():
    """Class to run the UI for phone application.

    When this type of object is created, it first turns on the GSM of the entire
    device.

    Attribute:
        signal (File): file whose contents determine if a call is incoming
    #   fona_error = open('fona_log.txt', 'w+') # might want to have this for if in call_thread.py or
                                                # sms_thread.py the FONA throws an exception in run()
                                                # (use as error log)
    """

    signal = open('signal.txt', 'w+')

    def __init__(self):
        pass

    def run(self):
        # create GUI here


        self.close_application()

    def close_application(self):
        """ close any files opened """
        #signal.close()

if __name__ == '__main__':
    ui = UI()
    ui.run()

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App

class PhoneApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return BoxLayout()

if __name__ == '__main__':
    home = PhoneApp()
    home.run()
