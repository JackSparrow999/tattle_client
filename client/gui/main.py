from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from poc.redis_client import redis_obj
from kivy.uix.button import Button
from kivy.uix.label import Label

from client.commands import main

import requests

class MyLabel(Label):
   def on_size(self, *args):
      self.text_size = self.size

class MainApp(App):

    latest_chats = None
    chat_box = None
    cmd_output = None
    cmd_input = None

    user_id = None
    user_name = None
    room_id = None
    room_name = None

    info = None

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
                        size_hint=(.65, .65),
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
                                pos_hint = {'x': .75, 'y': .35},
                                cursor_color=(1, 1, 1, 1))

        self.cmd_output = cmd_out

        # send button
        execute_btn = Button(text="Execute",
                          size_hint=(.2, .1),
                          background_color=(0.4, .7, 1, 1),
                          pos_hint={'x': .75, 'y': .2})
        execute_btn.bind(on_press=self.execute_button_callback)

        # info label
        info = MyLabel(text ="user_id: user_name: room_name: ",
            color =[0.41, 0.42, 0.74, 1],
            font_size='20sp',
            halign = 'left',
            pos_hint={'x': 0.05, 'y': .9})
        self.info = info

        global_window.add_widget(send_btn)
        global_window.add_widget(chat_view)
        global_window.add_widget(chat_input)
        global_window.add_widget(cmd_in)
        global_window.add_widget(cmd_out)
        global_window.add_widget(execute_btn)
        global_window.add_widget(info)

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

channel = 'chat_channel'

def publish(chat):
    redis_obj.publish(channel, chat)

def message_handler(message):
    if app.latest_chats.text == '':
        app.latest_chats.text = message["data"]
    else:
        app.latest_chats.text = app.latest_chats.text \
                                 + '\n' \
                                 + message["data"]

def execute_cmd(cmd):
    if switch_room(cmd) == False:
        output = main.route_command(cmd)
        login_user(cmd, output)
    else:
        output = 'switched to room ' + app.room_name
    app.info.text = "user_id: " + str(app.user_id) + "  user_name: " + str(app.user_name) + "  room_name: " + str(app.room_name)
    return output


def login_user(cmd, out):
    lst = cmd.split()
    user = None
    if lst[0] == 'login' and out == 'true':
        user = get_user_from_user_id(lst[1])
        app.user_id = user['user_id']
        app.user_name = user['user_name']
        app.room_name = None
        app.room_id = None
    print(user)


def get_user_from_user_id(user_id):
    cmd = main.Command()
    response = requests.get(cmd.build_url('/auth/user/'), params={
        'user_id': user_id
    })
    lst = response.json()['users']
    user_name = ''
    for x in lst:
        user_name = x['user_name']
    user = {'user_id': user_id, 'user_name': user_name}
    return user

#switch room_id
def switch_room(cmd):
    lst = cmd.split()
    if len(lst) < 1:
        return
    room_id = int(lst[1])
    if lst[0] == 'switch' and room_id != None:
        if check_room_member(room_id, app.user_id):
            room = get_room_from_room_id(room_id)
            app.room_id = room['room_id']
            app.room_name = room['room_name']

            app.latest_chats.text = ''

            global channel

            pub.unsubscribe(channel)
            channel = str(app.room_id)
            pub.subscribe(**{channel: message_handler})
            pub.run_in_thread(sleep_time=1)

        return True
    return False


def check_room_member(room_id, user_id):
    cmd = main.Command()
    response = requests.get(cmd.build_url('/auth/add_user/'), params={
        'room_id': room_id,
        'user_id': user_id
    })

    return response.json()["is_member"]


def get_room_from_room_id(room_id):
    cmd = main.Command()
    response = requests.get(cmd.build_url('/auth/room/'), params={
        'room_id': room_id
    })
    lst = response.json()['rooms']
    room_name = ''
    for x in lst:
        room_name = x['room_name']
    room = {'room_id': room_id, 'room_name': room_name}
    return room


if __name__ == '__main__':
    print(get_room_from_room_id(1))
    pub = redis_obj.pubsub()
    pub.subscribe(**{channel: message_handler})
    pub.run_in_thread(sleep_time=1)
    # while True:
    #
    #     try:
    app.run()
        # except:
            # continue