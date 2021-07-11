from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from poc.redis_client import redis_obj
from kivy.uix.button import Button

class MainApp(App):

    latest_chats = None
    chat_box = None

    def build(self):

        super_box = BoxLayout(orientation = 'vertical')

        #send button
        send_btn = Button(text="Send")
        send_btn.bind(on_press = self.send_button_callback)

        #info box
        info_box = BoxLayout(orientation='horizontal')

        chats = BoxLayout(orientation='horizontal')
        online_status = BoxLayout(orientation='horizontal')
        chat_view = TextInput(text='', multiline=True, readonly=True)
        self.latest_chats = chat_view
        online_info = TextInput(text='online is here',
                             size_hint=(.5, .5),
                             pos_hint={'center_x': .5, 'center_y': .5})
        chats.add_widget(chat_view)
        online_status.add_widget(online_info)
        info_box.add_widget(chats)
        info_box.add_widget(online_status)
        super_box.add_widget(info_box)


        #text box
        type_box = BoxLayout(orientation='horizontal')
        chat_input = TextInput(text='', multiline=False, text_validate_unfocus=False)
        chat_input.bind(on_text_validate=self.on_enter_in_chat)
        self.chat_box = chat_input
        # type_label = Label(text='Type something: ',
        #                    size_hint=(.5, .5),
        #                    pos_hint={'center_x': .5, 'center_y': .5})
        type_box.add_widget(chat_input)
        type_box.add_widget(send_btn)
        super_box.add_widget(type_box)

        return super_box


    def on_enter_in_chat(instance, value):
        if instance.latest_chats.text == '':
            instance.latest_chats.text = value.text
        else:
            instance.latest_chats.text = instance.latest_chats.text \
                                         + '\n' \
                                         + value.text
        value.text = ''

    def send_button_callback(self, event):
        if self.latest_chats.text == '':
            self.latest_chats.text = self.chat_box.text
        else:
            self.latest_chats.text = self.latest_chats.text \
                                         + '\n' \
                                         + self.chat_box.text
        self.chat_box.text = ''


app = MainApp()

def message_handler(message):
    if message == None:
        return None
    if app.latest_chats.text == '':
        app.latest_chats.text = message["data"]
    else:
        app.latest_chats.text = app.latest_chats.text \
                                + '\n' \
                                + message["data"]


if __name__ == '__main__':

    pub = redis_obj.pubsub()
    pub.subscribe(**{'hello_world': message_handler})
    pub.run_in_thread(sleep_time=1)
    app.run()