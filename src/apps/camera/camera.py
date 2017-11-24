#!/usr/bin/python
# camera.py

from io import BytesIO
from os import environ
from picamera import PiCamera
from time import sleep
from datetime import datetime, timedelta
import pygame
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen


class Camera():
    """Wrapper class to interact with the Raspberry Pi's camera hardware
    in order to capture and save photos as well as record videos.

    Attributes:
        WIDTH (int): width of the touch screen
        HEIGHT (int): height of the touch screen
        buttonHit (boolean): flag used whenever a button has been pressed in the UI
    """

    WIDTH = 480
    HEIGHT = 800
    buttonHit = False

    def __init__(self):
        """Constructor for Camera object.

        Sets environment for screen to SPI, configures PiCamera object.

        Attribute:
            camera (picamera.PiCamera): PiCamera object for this class to interact with
        """
        """Set screen to SPI"""
        environ['SDL_FDBEV'] = '/dev/fb1'
        environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
        environ['SDL_MOUSEDRV'] = 'TSLIB'

        """Configure Raspberry PiCamera for screen's dimensions"""
        self.camera = PiCamera()
        self.camera.resolution = (WIDTH, HEIGHT)
        self.camera.rotation = 180

    def capture(self):
        """Captures image from camera and saves to the Pictures directory."""
        sleep(2) # camera wake up time
        self.camera.capture('../Pictures/' + self.image_file_name() + '.jpg')
        """TODO: probably just want to name it after the current date so you don't have to worry about overwritting existing photos"""

    def image_file_name(self):
        """Reads the index file in order to find the current file name number and
        update that.

        In order to name photo files from the camera, names are a number
        followed by the appropriate file extension (1.jpg, 2.jpg, 3.jpg, ...)
        Returns string of the file name of the next image to be saved.
        """
        f = open('photo_index.txt', 'w+')
        try:
            index = int(f.readline())
            f.write(str(index + 1))
            f.close()
            return str(index)
        except ValueError:
            """empty file"""
            f.write('1')
            f.close()
            return '0'

    def video_file_name(self):
        """Reads the index file in order to find the current file name number and
        update that.

        In order to name video files from the camera, names are a number
        followed by the appropriate file extension (1.jpg, 2.jpg, 3.jpg, ...)
        Returns string of the file name of the next video to be saved.
        """
        f = open('video_index.txt', 'w+')
        try:
            index = int(f.readline())
            f.write(str(index + 1))
            f.close()
            return str(index)
        except ValueError:
            """empty file"""
            f.write('1')
            f.close()
            return '0'

    def display(self):
        """Method to display on the screen what the camera 'sees'"""
        while True:
            # self.camera.resolution = (1024, 768)
            """Buffer for screen color data"""
            rgb = bytearray(WIDTH * HEIGHT * 3)
            stream = BytesIO()
            self.camera.capture(stream, use_video_port=True, format='rgb')
            stream.seek(0)
            stream.readinto(rgb)
            stream.close()
            image = pygame.image.frombuffer(rgb[0:(WIDTH * HEIGHT * 3)], (WIDTH, HEIGHT), 'RGB')
            self.screen.blit(image, (0, 0))
            pygame.display.update()

    def record(self):
        # self.camera.resolution = (640, 480)
        self.camera.start_recording('../Videos/' + self.video_file_name() + '.h264')
        if (buttonHit):
            self.camera.stop_recording()

    def low_light(self):
        # camera.resolution = (1280, 720)
        """Set a framerate of 1/6fps, then set shutter speed to 6s and ISO to 800"""
        self.camera.framerate = Fraction(1, 1)
        self.camera.shutter_speed = 1000000
        self.camera.exposure_mode = 'off'
        self.camera.iso = 800
        # Give the camera a good long time to measure AWB
        # (you may wish to use fixed AWB instead)
        sleep(10)
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds
        self.camera.capture('dark.jpg')

    def wait(self):
        """Calculate the delay to the start of the next hour"""
        next_hour = (datetime.now() + timedelta(hour=1)).replace(minute=0, second=0, microsecond=0)
        delay = (next_hour - datetime.now()).seconds
        sleep(delay)

    def timelapse(self):
        self.camera.start_preview()
        self.wait()
        for file_name in self.camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
            print('Captured %s' % file_name)
            self.wait()

    def enable_flash(self):
        """Enables the Raspberry Pi's camera flash"""
        self.camera.flash_mode = 'on'

    def disable_flash(self):
        "Disables the Raspberry Pi's camera"
        self.camera.flash_mode = 'off'

    def close(self):
        """Method called whenever the camera UI is closed. Closes the Raspberry Pi's camera."""
        self.camera.close()

class RecordScreen(screen):
    pass

class CameraScreen(screen):
    pass

sm = ScreenManager()
sm.add_widget(CameraScreen(name='camera'))
sm.add_widget(RecordScreen(name='record'))

class CameraApp(App):
    def build(self):
        Window.fullscreen = True
        return sm

if __name__ == '__main__':
    CameraApp().run()
