import os
from Canvas import Rectangle

from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

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
