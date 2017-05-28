import kivy
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label


class HomeScreenApp(App):
    def build(self):
        #self.load_kv('Launcher.kv')
        return BoxLayout()


if __name__ == '__main__':
    home = HomeScreenApp()
    home.run()
