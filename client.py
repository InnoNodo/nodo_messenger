from socket import socket, AF_INET, SOCK_STREAM, error as SocketError
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
import threading

SERVER = "77.246.102.127"
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
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self, instance):
        message = self.message_input.text
        if message:
            try:
                client.sendall(message.encode('UTF-8'))
                self.message_input.text = ''
                self.add_message_to_log(f"You: {message}")  # Add message to log
            except SocketError as e:
                print(f"Error sending message: {e}")

    def add_message_to_log(self, message):
        label = Label(text=message, size_hint_y=None, height=40)
        self.message_log.add_widget(label)

    def receive_messages(self):
        while True:
            try:
                data = client.recv(4096).decode()
                if data:
                    Clock.schedule_once(lambda dt: self.add_message_to_log(data))
                else:
                    break
            except SocketError as e:
                print(f"Connection error: {e}")
                break
            except ConnectionError:
                print("Server disconnected.")
                break

        Clock.schedule_once(lambda dt: setattr(self.message_input, 'disabled', True))

class ChatApp(App):
    def build(self):
        return ChatLayout()

if __name__ == '__main__':
    ChatApp().run()
