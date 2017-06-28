
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


class BrowserApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return FloatLayout()

if __name__ == '__main__':
    home = BrowserApp()
    home.run()
