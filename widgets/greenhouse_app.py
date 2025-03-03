from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

class GreenhouseApp(FloatLayout):
    greenhouse_data = ObjectProperty(None)

    @property
    def total_plants(self):
        if self.greenhouse_data:
            return self.greenhouse_data.total_plants
        return 0

    @property
    def total_species(self):
        if self.greenhouse_data:
            return self.greenhouse_data.total_species
        return 0

    @property
    def available_spots(self):
        if self.greenhouse_data:
            return self.greenhouse_data.available_spots
        return 0
