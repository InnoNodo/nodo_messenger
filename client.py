from socket import socket, AF_INET, SOCK_STREAM
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

SERVER = "127.0.0.1"
PORT = 1488

client = socket(AF_INET, SOCK_STREAM)
client.connect((SERVER, PORT))

class ChatLayout(BoxLayout):
    chat_log = StringProperty("")

    def __init__(self, **kwargs):
        super(ChatLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'

        self.message_log = GridLayout(cols=1, size_hint_y=None)
        self.message_log.bind(minimum_height=self.message_log.setter('height'))

        scroll = ScrollView(size_hint=(1, 0.8))
        scroll.add_widget(self.message_log)
        self.add_widget(scroll)

        self.message_input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.message_input.bind(on_text_validate=self.send_message)
        self.add_widget(self.message_input)

        send_button = Button(text="Send", size_hint=(1, 0.1))
        send_button.bind(on_press=self.send_message)
        self.add_widget(send_button)

        Clock.schedule_interval(self.receive_messages, 1 / 20.0)

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            client.sendall(bytes(message, 'UTF-8'))
            self.message_input.text = ''

    def receive_messages(self, dt):
        try:
            data = client.recv(4096).decode()
            if data:
                self.message_log.add_widget(Label(text=f"Server: {data}", size_hint_y=None, height=40))
        except ConnectionError:
            pass

class ChatApp(App):
    def build(self):
        return ChatLayout()

if __name__ == '__main__':
    ChatApp().run()
