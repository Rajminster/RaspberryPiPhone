
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from cefpython3 import cefpython as cef
import platform
import sys

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout


def main():
    check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="https://www.google.com/",
                          window_title="Hello World!")
    cef.MessageLoop()
    cef.Shutdown()

def check_versions():
    print("[hello_world.py] CEF Python {ver}".format(ver=cef.__version__))
    print("[hello_world.py] Python {ver} {arch}".format(
          ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"


class BrowserApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return FloatLayout()

if __name__ == '__main__':
    #home = BrowserApp()
    #home.run()
    main()

