# plant_home_widgets.py
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, DictProperty
from kivy.app import App
from kivy.uix.popup import Popup

class PlantGridItemWidget(FloatLayout):
    display_name = StringProperty("")
    display_species = StringProperty("")
    # Reference to the popup that created this item.
    popup_ref = ObjectProperty(None)
    # Full plant data from the CSV.
    plant_data = DictProperty({})

    def on_select(self):
        # Use the CSV data and map CSV keys to our internal keys.
        new_plant = self.plant_data.copy()
        new_plant['plant_name'] = new_plant.get('common_name', 'Unknown')
        new_plant['plant_species'] = new_plant.get('type', 'Unknown Species')
        new_plant['plant_status'] = 'New'         # Set default status.
        new_plant['plant_location'] = 'Greenhouse'
        new_plant['plant_count'] = 1
        app = App.get_running_app()
        app.greenhouse_data.add_user_plant(new_plant)

        if self.popup_ref:
            self.popup_ref.dismiss()

        if hasattr(app.root, "get_screen"):
            try:
                plant_home_screen = app.root.get_screen("PlantHome")
                plant_home_screen.update_plant_list()
            except Exception as e:
                print("Error updating PlantHomeScreen:", e)
        elif hasattr(app.root, "update_plant_list"):
            app.root.update_plant_list()

class AddPlantPopup(Popup):
    def perform_search(self, search_text):
        """
        Filters the available plants based on the search text.
        """
        full_db = App.get_running_app().greenhouse_data.plant_database
        filtered_data = []
        for plant in full_db:
            common_name = plant.get('common_name', '').lower()
            species_type = plant.get('type', '').lower()
            if search_text.lower() in common_name or search_text.lower() in species_type:
                filtered_data.append({
                    'display_name': plant.get('common_name', 'Name'),
                    'display_species': plant.get('type', 'Species'),
                    'plant_data': plant,
                    'popup_ref': self,
                })
        if 'available_plants_rv' in self.ids:
            self.ids.available_plants_rv.data = filtered_data
