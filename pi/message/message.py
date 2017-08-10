
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.listview import ListView
from kivy.base import runTouchApp


class MainView(ListView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(
            item_strings=[str(index) for index in range(100)])
class MessageApp(App):
    def build(self):
        root = FloatLayout()
        Window.size = (480, 800)
        Window.fullscreen = False
        layout = BoxLayout(orientation='vertical', size=(480,700), size_hint=(None, None), pos = (0,70))
        for i in range(12):
            layout.add_widget(Button(text='Contact ' + str(i)))
        root.add_widget(layout)
        return root

if __name__ == '__main__':
    home = MessageApp()
    home.run()
    #runTouchApp(MainView())



