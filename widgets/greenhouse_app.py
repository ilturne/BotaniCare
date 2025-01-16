# widgets/greenhouse_app.py
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty

class GreenhouseApp(FloatLayout):
    """
    Root layout of the Greenhouse application. Contains references to plant stats.
    """
    total_plants = NumericProperty(0)
    total_species = NumericProperty(0)
    available_spots = NumericProperty(0)
