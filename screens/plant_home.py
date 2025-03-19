# plant_home.py
import json
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty
from widgets.plant_home_widgets import AddPlantPopup

class PlantListItem(BoxLayout):
    plant_id = StringProperty("")  # Must be a string
    plant_name = StringProperty("")
    plant_status = StringProperty("")
    plant_location = StringProperty("")
    plant_status_color = ListProperty([0.0, 0.0, 0.0, 1.0])
    plant_count = NumericProperty(0)
    plant_species = StringProperty("")
    # Local remove_mode property, bound from the parent screen.
    remove_mode = BooleanProperty(False)

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

    def handle_action(self):
        # This method is called when the remove/details button is pressed.
        from kivy.app import App
        app = App.get_running_app()
        if self.remove_mode:
            # Instead of directly calling greenhouse_data.remove_user_plant,
            # retrieve the PlantHomeScreen and call its remove_plant() method.
            if hasattr(app.root, "get_screen"):
                try:
                    plant_home_screen = app.root.get_screen("PlantHome")
                    plant_home_screen.remove_plant(self.plant_id)
                except Exception as e:
                    print("Error updating PlantHomeScreen:", e)
            else:
                app.greenhouse_data.remove_user_plant(self.plant_id)
                app.root.update_plant_list()
        else:
            print(f"Details for {self.plant_name}")

class PlantHomeScreen(Screen):
    # Toggle for removal mode.
    remove_mode = BooleanProperty(False)

    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        self.greenhouse_data._update_title_text()
        self.populate_plant_list()
        
    def populate_plant_list(self):
        rv = self.ids.plant_rv
        user_plants = self.greenhouse_data.user_added_plants

        rv_items = []
        if user_plants:
            for plant in user_plants:
                # Convert the id to string to satisfy the StringProperty.
                entry = {
                    'plant_id': str(plant.get('id', '')),
                    'plant_name': plant.get('plant_name', 'Unknown'),
                    'plant_status': plant.get('plant_status', 'Unknown'),
                    'plant_location': plant.get('plant_location', 'Unknown'),
                    'plant_species': plant.get('plant_species', 'Unknown Species'),
                    'plant_count': plant.get('plant_count', 0),
                    'remove_mode': self.remove_mode,
                }
                # Create an instance to update its status color.
                item = PlantListItem(**entry)
                item.update_status_color()
                rv_items.append({
                    'plant_id': item.plant_id,
                    'plant_name': item.plant_name,
                    'plant_status': item.plant_status,
                    'plant_species': item.plant_species,
                    'plant_location': item.plant_location,
                    'plant_status_color': item.plant_status_color,
                    'plant_count': item.plant_count,
                    'remove_mode': self.remove_mode,
                })
        else:
            default_entry = {
                'plant_id': "",
                'plant_name': "Click Add",
                'plant_status': "Ready for Harvest",
                'plant_species': "Example",
                'plant_location': "Isle X Bay X",
                'plant_count': 4,
                'remove_mode': self.remove_mode,
            }
            item = PlantListItem(**default_entry)
            item.update_status_color()
            rv_items.append({
                'plant_id': item.plant_id,
                'plant_name': item.plant_name,
                'plant_status': item.plant_status,
                'plant_species': item.plant_species,
                'plant_location': item.plant_location,
                'plant_status_color': item.plant_status_color,
                'plant_count': item.plant_count,
                'remove_mode': self.remove_mode,
            })

        rv.data = rv_items

    def update_plant_list(self):
        self.populate_plant_list()

    def remove_plant(self, plant_id):
    # If there is only one plant left, clear the list and reset counts.
        if len(self.greenhouse_data.user_added_plants) <= 1:
            self.greenhouse_data.user_added_plants = []
            self.greenhouse_data.healthy_species = 0
            self.greenhouse_data.total_species = 0
            self.greenhouse_data.save_user_plants()
            self.greenhouse_data._update_title_text()  # Update title_text to reflect zero plants.
        else:
            self.greenhouse_data.remove_user_plant(plant_id)
        self.update_plant_list()


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
        
