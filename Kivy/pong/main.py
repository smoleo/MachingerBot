from kivy.app import App
from kivy.uix.widget import Widget

# https://kivy.org/doc/stable/tutorials/pong.html

class PongGame(Widget):
    pass

#name of .kv must be App name without App in this case pong
class PongApp(App):
    def build(self):
        return PongGame()

if __name__ == '__main__':
    PongApp().run()