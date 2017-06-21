
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App

class BrowserApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return BoxLayout()

if __name__ == '__main__':
    home = BrowserApp()
    home.run()
