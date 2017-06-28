<<<<<<< HEAD
import os
from Canvas import Rectangle

from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.uix.boxlayout import BoxLayout
=======
from kivy.core.audio import SoundLoader

# need to define clicked in UI
>>>>>>> d0565c01038d8814199a5171e5e31ee39e20a895

sound = SoundLoader.load(clicked)

<<<<<<< HEAD
from kivy.app import App
from os.path import dirname, abspath

from kivy.uix.floatlayout import FloatLayout


class MusicApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        par = dirname(dirname(abspath(__file__)))
        return FloatLayout()

if __name__ == '__main__':
    home = MusicApp()
    home.run()
=======
if sound:
    sound.play()
>>>>>>> d0565c01038d8814199a5171e5e31ee39e20a895
