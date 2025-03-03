# settings_screen.py
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty

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

    def on_pre_enter(self, *args):
        # Update the local properties from the shared data when entering the screen
        self.greenhouse_name = self.greenhouse_data.greenhouse_name
        self.greenhouse_unit = self.greenhouse_data.greenhouse_units
        self.greenhouse_num_rows = self.greenhouse_data.layout_rows
        self.greenhouse_num_colm = self.greenhouse_data.layout_cols

    def on_pre_leave(self, *args):
        # Before leaving, propagate any changes back to the shared data and save state.
        self.greenhouse_data.greenhouse_name = self.greenhouse_name
        self.greenhouse_data.greenhouse_units = self.greenhouse_unit
        self.greenhouse_data.layout_rows = self.greenhouse_num_rows
        self.greenhouse_data.layout_cols = self.greenhouse_num_colm
        self.greenhouse_data.save_state()

    def greenhouse_unit_switch(self):
        if self.greenhouse_unit == "Metric":
            self.greenhouse_unit = "Imperial"
        else:
            self.greenhouse_unit = "Metric"

    def validate_row_input(self, new_text):
        filtered = "".join(ch for ch in new_text if ch.isdigit())[:2]
        self.ids.row_input.text = filtered
        self.greenhouse_num_rows = int(filtered) if filtered else 0

    def validate_col_input(self, new_text):
        filtered = "".join(ch for ch in new_text if ch.isdigit())[:2]
        self.ids.col_input.text = filtered
        self.greenhouse_num_colm = int(filtered) if filtered else 0
