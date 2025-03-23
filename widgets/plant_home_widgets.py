# plant_home_widgets.py
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ObjectProperty, DictProperty, ListProperty
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
        # Import the new quantity popup (ensure your project structure allows this import)
        from widgets.plant_home_widgets import PlantQuantityPopup
        app = App.get_running_app()
        # Convert CSV data to your internal format.
        new_plant = self.plant_data.copy()
        new_plant['plant_name'] = new_plant.get('common_name', 'Unknown')
        new_plant['plant_species'] = new_plant.get('type', 'Unknown Species')
        new_plant['plant_status'] = 'New'         # Default status.
        new_plant['plant_location'] = 'Greenhouse'
        new_plant['plant_count'] = 1
        
        # Instantiate the quantity popup.
        quantity_popup = PlantQuantityPopup()
        # Generate the row and column options dynamically from numeric values.
        quantity_popup.rows = [str(i) for i in range(1, app.greenhouse_data.layout_rows + 1)]
        quantity_popup.columns = [str(i) for i in range(1, app.greenhouse_data.layout_cols + 1)]
        # Pass along the plant data.
        quantity_popup.plant_data = new_plant
        quantity_popup.open()

        # Optionally dismiss the originating popup (if any).
        if self.popup_ref:
            self.popup_ref.dismiss()

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

class PremiumOnlyPopup(Popup):
    pass

class PlantQuantityPopup(Popup):
    rows = ListProperty([])     # Options for rows generated from layout_rows.
    columns = ListProperty([])  # Options for columns generated from layout_cols.
    plant_data = DictProperty({})  # Store plant info passed from the grid item.

    def on_confirm(self, quantity, row, column):
        try:
            quantity = int(quantity)
        except ValueError:
            print("Invalid quantity provided.")
            return
        app = App.get_running_app()
        new_plant = self.plant_data.copy()
        new_plant['plant_count'] = quantity
        # Format the plant_location based on the selected row and column.
        new_plant['plant_location'] = f"Row {row}, Col {column}"
        # Add the new plant to your user plants.
        app.greenhouse_data.add_user_plant(new_plant)

        if hasattr(app.root, "get_screen"):
            try:
                plant_home_screen = app.root.get_screen("PlantHome")
                plant_home_screen.update_plant_list()
            except Exception as e:
                print("Error updating PlantHomeScreen:", e)
        elif hasattr(app.root, "update_plant_list"):
            app.root.update_plant_list()
            
        self.dismiss()
