import kivy
from kivy.config import Config

# Set the window size for the Raspberry Pi screen
Config.set('graphics', 'width', '800')  # Width of the Window
Config.set('graphics', 'height', '480')  # Height of the Window

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout  # Import FloatLayout
from kivy.uix.boxlayout import BoxLayout        # **Ensure BoxLayout is imported**
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

# Load the KV file
Builder.load_file('greenhouse.kv')

class GreenhouseApp(FloatLayout):  # Inherits from FloatLayout as defined in KV
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plants = []

    def add_plant(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))  # BoxLayout used here
        input_field = TextInput(hint_text='Enter plant name', multiline=False)
        buttons = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(10))

        btn_add = Button(text='Add', on_press=lambda x: self.add_plant_to_list(input_field.text))
        btn_cancel = Button(text='Cancel', on_press=lambda x: self.popup.dismiss())
        buttons.add_widget(btn_add)
        buttons.add_widget(btn_cancel)

        content.add_widget(Label(text='Add a new plant'))
        content.add_widget(input_field)
        content.add_widget(buttons)

        self.popup = Popup(title='Add Plant', content=content, size_hint=(0.8, 0.4))
        self.popup.open()

    def add_plant_to_list(self, plant_name):
        if plant_name.strip():
            self.plants.append(plant_name.strip())
            self.update_plant_list()
            self.ids.status_label.text = f'{plant_name} added.'
        else:
            self.ids.status_label.text = 'Plant name cannot be empty.'
        self.popup.dismiss()

    def remove_plant(self):
        if self.plants:
            plant_name = self.plants.pop()
            self.update_plant_list()
            self.ids.status_label.text = f'{plant_name} removed.'
        else:
            self.ids.status_label.text = 'No plants to remove.'

    def update_plant_list(self):
        self.ids.plant_list.clear_widgets()
        for plant in self.plants:
            self.ids.plant_list.add_widget(
                Label(
                    text=plant,
                    size_hint_y=None,
                    height=dp(30),
                    halign='left',
                    valign='middle',
                    text_size=(self.width, None)
                )
            )

    def check_status(self):
        self.ids.status_label.text = 'Check Status button pressed.'
        # Implement code to check sensor status

    def open_settings(self):
        self.ids.status_label.text = 'Settings button pressed.'
        # Implement settings functionality here

class MyApp(App):
    def build(self):
        return GreenhouseApp()

if __name__ == '__main__':
    MyApp().run()
