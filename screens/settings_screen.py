# settings_screen.py

from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.textinput import TextInput

class SettingsScreen(Screen):
    """
    The settings screen that allows users to configure the greenhouse settings.
    """
    greenhouse_name = StringProperty("")
    greenhouse_unit = StringProperty("Imperial")
    greenhouse_num_rows = NumericProperty(0)
    greenhouse_num_colm = NumericProperty(0)
    
    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data
        
    def greenhouse_unit_switch(self):
        if self.greenhouse_unit == "Metric":
            self.greenhouse_unit = "Imperial"
        else:
            self.greenhouse_unit = "Metric"

    def validate_row_input(self, new_text):
        filtered = "".join(ch for ch in new_text if ch.isdigit())
        filtered = filtered[:2]
        self.ids.row_input.text = filtered
        self.greenhouse_num_rows = int(filtered) if filtered else 0

    def validate_col_input(self, new_text):
        filtered = "".join(ch for ch in new_text if ch.isdigit())
        filtered = filtered[:2]
        self.ids.col_input.text = filtered
        self.greenhouse_num_colm = int(filtered) if filtered else 0
