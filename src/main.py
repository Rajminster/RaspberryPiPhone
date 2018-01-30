from glob import glob
from os.path import dirname, join

import kivy
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Logger
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage, Image
from kivy.graphics import *
from apps.gallery.gallery import GalleryApp
from apps.message.message import MessageApp
import multiprocessing
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition, CardTransition


class ScreenManagement(ScreenManager):
    ScreenManager.transition = CardTransition()
    pass


class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.on_enter()

    def switch(self):
        # here you can insert any python logic you like
        self.parent.current = 'Test'

    @mainthread
    def on_enter(self):
        layout = self.ids.list
        image = Image(source='resources/Home_Button.png', allow_stretch=False, pos=(0, -365))
        button = HomeButton(size_hint=(.1, .06), pos=(216, 12))
        button.opacity = 0.5
        layout.add_widget(button)
        layout.add_widget(image)


class Test(Screen):
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)
        self.on_enter()

    def switch(self):
        # here you can insert any python logic you like
        self.parent.current = 'Home'

    @mainthread
    def on_enter(self):
        layout = self.ids.convo
        image = Image(source='resources/Home_Button.png', allow_stretch=False, pos=(0, -365))
        button = HomeButton(size_hint=(.1, .06), pos=(216, 12))
        button.opacity = 0.5
        layout.add_widget(button)
        layout.add_widget(image)


class HomeScreen(App):
    def build(self):
        # Builder.load_file('HomeScreen.kv')
        root = FloatLayout()
        Window.size = (480, 800)
        Window.fullscreen = False
        # Window.borderless = True

        # get any files into images directory
        # 75 from left, 160 between
        x = 30
        y = 395
        col = 1

        image = Image(source='resources/Home_Button.png', allow_stretch=False, pos=(0, -365))
        button = HomeButton(size_hint=(.1, .06), pos=(216, 12))
        button.opacity = 0.5
        root.add_widget(button)
        root.add_widget(image)
        return ScreenManagement()


class HomeButton(Button):
    def __init__(self, **kwargs):
        super(HomeButton, self).__init__(**kwargs)

    def on_press(self):
        # app = MessageApp()
        # p = multiprocessing.Process(target=app.run)
        # p.start()
        pass

    def on_release(self):
        pass


if __name__ == '__main__':
    home = HomeScreen()
    home.run()
