from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from poc.redis_client import redis_obj
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainApp(App):

    latest_chats = None
    chat_box = None

    def build(self):

        global_window = FloatLayout()

        #send button
        send_btn = Button(text="Send",
                        size_hint=(.2, .1),
                        background_color=(0.298, .6, 0, 1),
                        pos_hint={'x': .75, 'y': .05})
        send_btn.bind(on_press = self.send_button_callback)

        #global chat view
        chat_view = TextInput(text='', multiline=True, readonly=True,
                        size_hint=(.65, .75),
                        background_color=(1, 1, .8, 1),
                        pos_hint={'x': .05, 'y': .2},
                        cursor_color=(1, 1, .8, 1))
        self.latest_chats = chat_view

        #online info of users
        online_info = TextInput(text='online is here',
                        size_hint=(.2, .75),
                        background_color=(.8, .8, 1, 1),
                        pos_hint={'x': .75, 'y': .2})

        #chat input window
        chat_input = TextInput(text='', multiline=False, text_validate_unfocus=False,
                        size_hint=(.65, .1),
                        background_color=(0.753, 0.753, 0.753, 1),
                        pos_hint={'x': .05, 'y': .05})
        chat_input.bind(on_text_validate=self.on_enter_in_chat)
        self.chat_box = chat_input

        global_window.add_widget(send_btn)
        global_window.add_widget(chat_view)
        global_window.add_widget(chat_input)
        global_window.add_widget(online_info)

        return global_window


    def on_enter_in_chat(instance, value):
        publish(value.text)
        value.text = ''

    def send_button_callback(self, event):
        publish(self.chat_box.text)
        self.chat_box.text = ''


app = MainApp()

def publish(chat):
    redis_obj.publish('chat_channel', chat)

def message_handler(message):
    if app.latest_chats.text == '':
        app.latest_chats.text = message["data"]
    else:
        app.latest_chats.text = app.latest_chats.text \
                                 + '\n' \
                                 + message["data"]


if __name__ == '__main__':

    pub = redis_obj.pubsub()
    pub.subscribe(**{'chat_channel': message_handler})
    pub.run_in_thread(sleep_time=1)
    app.run()