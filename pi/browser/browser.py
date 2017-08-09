
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
import platform
import sys

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from cefbrowser import CEFBrowser
from tabbed import TabbedCEFBrowser

class BrowserApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return TabbedCEFBrowser(
                urls=[
                    "http://keh.com"
                ],
                pos=(0, 0),
                size_hint=(None, None),
                # size=(Window.width-40, Window.height-20),
                size=(480, 800),
            )

if __name__ == '__main__':
    home = BrowserApp()
    home.run()


