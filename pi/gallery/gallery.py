import kivy
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage, Image
from kivy.config import Config
from kivy.core.window import Window


# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from os.path import dirname, join

from setuptools.glob import glob


class GalleryApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        layout = BoxLayout(orientation = 'vertical')
        carousel = Carousel(direction='right')
        layout.add_widget(carousel)
        b = BackButton(text='Back ', size_hint = (None, None), size =(100,50))
        layout.add_widget(b)
        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'DCIM', '*')):
            image = AsyncImage(source=filename, allow_stretch=True)
            carousel.add_widget(image)
        return layout
        #return BoxLayout()




class BackButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)

    def on_press(self):
        pass

    def on_release(self):
        App.get_running_app().stop()


if  __name__ =='__main__':
    home = GalleryApp()
    home.run()
    Config.getint('kivy', 'show_fps')

