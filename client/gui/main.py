from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from poc.redis_client import redis_obj
from kivy.uix.button import Button

from client.commands import main

class MainApp(App):

    latest_chats = None
    chat_box = None
    cmd_output = None
    cmd_input = None

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

        #chat input window
        chat_input = TextInput(text='Enter message', multiline=False, text_validate_unfocus=False,
                        size_hint=(.65, .1),
                        background_color=(0.753, 0.753, 0.753, 1),
                        pos_hint={'x': .05, 'y': .05})
        chat_input.bind(on_text_validate=self.on_enter_in_chat)
        self.chat_box = chat_input

        # cmd input
        cmd_in = TextInput(text='Enter command', multiline=False, text_validate_unfocus=False,
                           size_hint=(.2, .35),
                           background_color=(.8, .8, 1, 1),
                           pos_hint={'x': .75, 'y': .6})

        cmd_in.bind(on_text_validate=self.on_enter_in_cmd_input)

        self.cmd_input = cmd_in

        # cmd output
        cmd_out = TextInput(text='Command output', multiline=True, readonly=True,
                                size_hint = (.2, .2),
                                background_color = (1, 1, 1, 1),
                                pos_hint = {'x': .75, 'y': .35})

        self.cmd_output = cmd_out

        # send button
        execute_btn = Button(text="Execute",
                          size_hint=(.2, .1),
                          background_color=(0.4, .7, 1, 1),
                          pos_hint={'x': .75, 'y': .2})
        execute_btn.bind(on_press=self.execute_button_callback)

        global_window.add_widget(send_btn)
        global_window.add_widget(chat_view)
        global_window.add_widget(chat_input)
        global_window.add_widget(cmd_in)
        global_window.add_widget(cmd_out)
        global_window.add_widget(execute_btn)

        return global_window


    def on_enter_in_chat(instance, value):
        publish(value.text)
        value.text = ''

    def send_button_callback(self, event):
        publish(self.chat_box.text)
        self.chat_box.text = ''

    def on_enter_in_cmd_input(instance, value):
        output = execute_cmd(value.text)
        value.text = ''
        app.cmd_output.text = output

    def execute_button_callback(self, event):
        output = execute_cmd(self.cmd_input.text)
        self.cmd_input.text = ''
        self.cmd_output.text = output


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

def execute_cmd(cmd):
    output = main.route_command(cmd)
    print(output)
    return output


if __name__ == '__main__':

    pub = redis_obj.pubsub()
    pub.subscribe(**{'chat_channel': message_handler})
    pub.run_in_thread(sleep_time=1)
    app.run()