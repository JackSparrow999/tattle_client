from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):

        super_box = BoxLayout(orientation = 'vertical')

        #info box
        info_box = BoxLayout(orientation='horizontal')

        chats = BoxLayout(orientation='horizontal')
        online_status = BoxLayout(orientation='horizontal')
        chat_label = Label(text='Chat is here',
                           size_hint=(.5, .5),
                           pos_hint={'center_x': .5, 'center_y': .5})
        online_label = Label(text='online is here',
                             size_hint=(.5, .5),
                             pos_hint={'center_x': .5, 'center_y': .5})
        chats.add_widget(chat_label)
        online_status.add_widget(online_label)
        info_box.add_widget(chats)
        info_box.add_widget(online_status)
        super_box.add_widget(info_box)


        #text box
        type_box = BoxLayout(orientation='horizontal')
        text_input = TextInput(text='', multiline=False, text_validate_unfocus=False)
        text_input.bind(on_text_validate=self.on_enter_in_chat)
        type_label = Label(text='Type something: ',
                           size_hint=(.5, .5),
                           pos_hint={'center_x': .5, 'center_y': .5})
        type_box.add_widget(text_input)
        type_box.add_widget(type_label)
        super_box.add_widget(type_box)

        return super_box


    def on_enter_in_chat(instance, value):
        print('Text: ', value.text)
        value.text = ''


if __name__ == '__main__':
    app = MainApp()
    app.run()