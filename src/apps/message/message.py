from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.listview import ListView
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager,Screen, SwapTransition, CardTransition
class MessageApp(App):
    def build(self):
        root = FloatLayout()
        Window.size = (480, 800)
        Window.fullscreen = False
        layout = BoxLayout(orientation='vertical', size=(480,700), size_hint=(None, None), pos = (0,70))
        for i in range(12):
            layout.add_widget(Button(text='Contact ' + str(i)))
        root.add_widget(layout)
        # return root
        return ScreenManagement()

class ScreenManagement(ScreenManager):
    ScreenManager.transition =  CardTransition()
    pass

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne,self).__init__(**kwargs)
        self.on_enter()
    def switch(self):
        #here you can insert any python logic you like
        self.parent.current = 'Second'
    @mainthread
    def on_enter(self):
        layout = self.ids.list
        button = HomeButton(size_hint=(.47, .47), pos=(212, 11), size=(50,50))
        button.opacity = 0.1
        image = Image(source='Home_Button.png', allow_stretch=False, pos=(0, -365))
        layout.add_widget(button)

class ScreenTwo(Screen):
    def __init__(self, **kwargs):
        super(ScreenTwo,self).__init__(**kwargs)
        self.on_enter()
    def switch(self):
        #here you can insert any python logic you like
        self.parent.current = 'First'

    @mainthread
    def on_enter(self):
        layout = self.ids.convo
        button = HomeButton(size_hint=(.47, .47), pos=(212, 11), size=(50,50))
        button.opacity = 0.1
        image = Image(source='Home_Button.png', allow_stretch=False, pos=(0, -365))
        layout.add_widget(button)


class HomeButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(HomeButton, self).__init__(**kwargs)

    def on_press(self):
        App.stop()

    def on_release(self):
        pass

class TestClass():
    def __init__(self, lay):
        layout = lay
        l = Label(text='Fuck YEA')
        layout.add_widget(l)
        print("RAN")


if __name__ == '__main__':
    home = MessageApp()
    home.run()
    #runTouchApp(MainView())



