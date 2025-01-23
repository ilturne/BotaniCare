from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.app import App

class PlantListItem(BoxLayout):
    plant_name = StringProperty("")
    plant_status = StringProperty("")
    plant_location = StringProperty("")
    plant_status_color = ListProperty([0.0, 0.0, 0.0, 1.0])  # Default color is black
    plant_count = NumericProperty(0)  # New property for plant count

    def update_status_color(self):
        """Update the plant_status_color based on the current plant_status."""
        if self.plant_status == "Ready for Harvest":
            self.plant_status_color = [13 / 255, 168 / 255, 8 / 255, 1]  # #0DA808
        elif self.plant_status == "Critical":
            self.plant_status_color = [1.0, 0.0, 0.0, 1]  # #FF0000
        elif self.plant_status == "Needs Attention":
            self.plant_status_color = [1.0, 95 / 255, 21 / 255, 1]  # #FF5F15
        elif self.plant_status == "Growing":
            self.plant_status_color = [117 / 255, 156 / 255, 74 / 255, 1]  # #759C4A
        else:
            self.plant_status_color = [0.5, 0.5, 0.5, 1]  # Default Grey for Unknown


class PlantHomeScreen(Screen):
    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        # Populate the RecycleView with a sample entry
        self.populate_plant_list()

    def populate_plant_list(self):
        rv = self.ids.plant_rv
        app = App.get_running_app()

        if app.user_added_plants:
            plant = app.user_added_plants[0]
            entry = {
                'plant_name': plant.get('common_name', 'Unknown'),
                'plant_status': plant.get('status', 'Unknown'),
                'plant_location': plant.get('location', 'Unknown'),
                'plant_count': plant.get('count', 0),  # Get count from data
            }
        else:
            entry = {
                'plant_name': "Example Plant",
                'plant_status': "Ready for Harvest",
                'plant_location': "Isle 1 Bay 1",
                'plant_count': 4,  # Example count
            }

        # Dynamically set the color for each status
        item = PlantListItem(**entry)
        item.update_status_color()

        # Assign data to RecycleView
        rv.data = [{'plant_name': item.plant_name,
                    'plant_status': item.plant_status,
                    'plant_location': item.plant_location,
                    'plant_status_color': item.plant_status_color,
                    'plant_count': item.plant_count}]

    def sort_by(self, criteria):
        print(f"Sorting by {criteria}")
        # Add sorting logic here

    def open_add_popup(self):
        """Opens the popup to add a new plant."""
        popup_content = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Add a label
        popup_content.add_widget(Label(text="Add New Plant", font_size="25sp"))

        # Add a button to close the popup
        close_button = Button(
            text="X",
            font_size="20sp",
            size_hint=(None, None),
            size=(60, 40),
            pos_hint={'center_x': 0.5}
        )
        close_button.bind(on_release=lambda *args: popup.dismiss())

        popup_content.add_widget(close_button)

        # Create the popup
        popup = Popup(
            title="Add a New Plant",
            content=popup_content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
            background_color=[1, 1, 1, 1],
            background='',
            separator_height=0,
        )
        popup.open()
