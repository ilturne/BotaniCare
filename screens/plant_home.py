from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.app import App
from kivy.factory import Factory

class PlantListItem(BoxLayout):
    plant_name = StringProperty("")
    plant_status = StringProperty("")
    plant_location = StringProperty("")
    plant_status_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    plant_count = NumericProperty(0)

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

        # Access user plants from greenhouse_data, not the app
        user_plants = self.greenhouse_data.user_added_plants
        if user_plants:
            plant = user_plants[0]
            entry = {
                'plant_name': plant.get('common_name', 'Unknown'),
                'plant_status': plant.get('status', 'Unknown'),
                'plant_location': plant.get('location', 'Unknown'),
                'plant_count': plant.get('count', 0),
            }
        else:
            entry = {
                'plant_name': "Example Plant",
                'plant_status': "Ready for Harvest",
                'plant_location': "Isle 1 Bay 1",
                'plant_count': 4,
            }

        item = PlantListItem(**entry)
        item.update_status_color()

        rv.data = [{
            'plant_name': item.plant_name,
            'plant_status': item.plant_status,
            'plant_location': item.plant_location,
            'plant_status_color': item.plant_status_color,
            'plant_count': item.plant_count
        }]

    def sort_by(self, criteria):
        print(f"Sorting by {criteria}")
        # Sorting logic if needed

    def open_add_popup(self):
        add_popup = Factory.AddPlantPopup()
        rv = add_popup.ids.available_plants_rv

        # Use greenhouse_data.plant_database to list all plants
        full_db = self.greenhouse_data.plant_database

        rv.data = [{
        'display_name': plant.get('common_name', 'Name'),
        'display_species': plant.get('type', 'Species')
    } for plant in full_db]

        def perform_search(search_text):
            filtered = []
            for plant in full_db:
                if search_text.lower() in plant['common_name'].lower():
                    filtered.append(plant)
            rv.data = [{
                'display_name': p.get('common_name', 'Name'),
                'display_species': p.get('species', 'Species'),
            } for p in filtered]

        add_popup.perform_search = perform_search
        add_popup.open()
