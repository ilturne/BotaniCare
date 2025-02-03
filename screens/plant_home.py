# plant_home.py
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty
from widgets.plant_home_widgets import AddPlantPopup

class PlantListItem(BoxLayout):
    plant_name = StringProperty("")
    plant_status = StringProperty("")
    plant_location = StringProperty("")
    plant_status_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    plant_count = NumericProperty(0)
    plant_species = StringProperty("")

    def update_status_color(self):
        if self.plant_status == "Ready for Harvest":
            self.plant_status_color = [13 / 255, 168 / 255, 8 / 255, 1]  # #0DA808
        elif self.plant_status == "Critical":
            self.plant_status_color = [1.0, 0.0, 0.0, 1]  # #FF0000
        elif self.plant_status == "Needs Attention":
            self.plant_status_color = [1.0, 95 / 255, 21 / 255, 1]  # #FF5F15
        elif self.plant_status == "Growing":
            self.plant_status_color = [117 / 255, 156 / 255, 74 / 255, 1]  # #759C4A
        else:
            self.plant_status_color = [0.5, 0.5, 0.5, 1]  # Default grey

class PlantHomeScreen(Screen):
    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.populate_plant_list()

    def populate_plant_list(self):
        rv = self.ids.plant_rv
        user_plants = self.greenhouse_data.user_added_plants

        rv_items = []
        if user_plants:
            for plant in user_plants:
                # Expecting keys added when the plant was selected.
                entry = {
                    'plant_name': plant.get('plant_name', 'Unknown'),
                    'plant_status': plant.get('plant_status', 'Unknown'),
                    'plant_location': plant.get('plant_location', 'Unknown'),
                    'plant_species': plant.get('plant_species', 'Unknown Species'),
                    'plant_count': plant.get('plant_count', 0),
                }
                item = PlantListItem(**entry)
                item.update_status_color()
                rv_items.append({
                    'plant_name': item.plant_name,
                    'plant_status': item.plant_status,
                    'plant_species': item.plant_species,
                    'plant_location': item.plant_location,
                    'plant_status_color': item.plant_status_color,
                    'plant_count': item.plant_count
                })
        else:
            default_entry = {
                'plant_name': "Example Plant",
                'plant_status': "Ready for Harvest",
                'plant_species': "Unknown Species",
                'plant_location': "Isle 1 Bay 1",
                'plant_count': 4,
            }
            item = PlantListItem(**default_entry)
            item.update_status_color()
            rv_items.append({
                'plant_name': item.plant_name,
                'plant_status': item.plant_status,
                'plant_species': item.plant_species,
                'plant_location': item.plant_location,
                'plant_status_color': item.plant_status_color,
                'plant_count': item.plant_count
            })

        rv.data = rv_items

    def update_plant_list(self):
        self.populate_plant_list()

    def sort_by(self, criteria):
        print(f"Sorting by {criteria}")
        # Add sorting logic if needed

    def open_add_popup(self):
        popup = AddPlantPopup()
        rv_data = []
        # Populate the popup using the public plant database (CSV).
        for plant in self.greenhouse_data.plant_database:
            rv_data.append({
                'display_name': plant.get('common_name', 'Unknown'),
                'display_species': plant.get('type', 'Unknown'),
                'plant_data': plant,  # Entire CSV row as a dictionary.
                'popup_ref': popup,
            })
        popup.ids.available_plants_rv.data = rv_data
        popup.open()
