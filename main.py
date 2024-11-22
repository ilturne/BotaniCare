from kivy.config import Config

# Set the window size for the Raspberry Pi touch screen
Config.set('graphics', 'width', '1280')  # Window width
Config.set('graphics', 'height', '720')  # Window height

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.clock import Clock
import random

# Load the KV file
Builder.load_file('greenhouse.kv')

class StatusCard(FloatLayout):
    """
    Custom widget representing a status card with a title, value, background color,
    ring color, and a customizable font size for the value label.
    """
    title = StringProperty('NO_TITLE')  # Card title
    value = StringProperty('--')        # Value displayed on the card
    ring_color = ListProperty([0.3, 0.6, 0.3, 0.8])  # Default ring color
    bg_color = ListProperty([0.78, 0.85, 0.68, 0.9])  # Default background color
    value_font_size = NumericProperty(30)  # Default font size for the value label

class GreenhouseApp(FloatLayout):
    """
    Main application widget that serves as the root layout.
    """
    pass

class MyApp(App):
    """
    The main application class that builds and runs the app.
    """
    def build(self):
        self.greenhouse_app = GreenhouseApp()

        # Initialize simulation variables
        self.current_temperature = 75.0
        self.temperature_increasing = True

        self.current_humidity = 0.50
        self.humidity_increasing = True

        self.current_light_level = 300.0  # Example value in lux
        self.light_level_increasing = True

        self.current_soil_moisture = 0.30  # Example value as a percentage
        self.soil_moisture_increasing = True

        # Schedule functions to simulate the environment
        Clock.schedule_interval(self.simulate_temperature, 0.2)
        Clock.schedule_interval(self.simulate_humidity, 0.2)
        Clock.schedule_interval(self.simulate_light_level, 0.2)
        Clock.schedule_interval(self.simulate_soil_moisture, 0.2)

        return self.greenhouse_app

    def simulate_temperature(self, dt):
        """
        Simulate the temperature fluctuating between 75°F and 80°F.
        """
        if self.temperature_increasing:
            self.current_temperature += 0.1
            if self.current_temperature >= 80.0:
                self.temperature_increasing = False
        else:
            self.current_temperature -= 0.1
            if self.current_temperature <= 75.0:
                self.temperature_increasing = True

        # Update the temperature display in the GreenhouseApp
        self.greenhouse_app.ids.temperature_card.value = f"{self.current_temperature:.1f}°F"

    def simulate_humidity(self, dt):
        """
        Simulate the humidity fluctuating between 40% and 60%.
        """
        self.humidity_increasing = 10
        if self.current_humidity >= 0.90:
            self.current_humidity = 0.40
        else:
            self.current_humidity += 0.01
            self.current_humidity = random.uniform(0.40, 0.90)
        # Update the humidity display in the GreenhouseApp
        self.greenhouse_app.ids.humidity_card.value = f"{self.current_humidity:.0%}"

    def simulate_light_level(self, dt):
        """
        Simulate the light level fluctuating between 200 and 800 lux.
        """
        if self.light_level_increasing:
            self.current_light_level += 10
            if self.current_light_level >= 800:
                self.light_level_increasing = False
        else:
            self.current_light_level -= 10
            if self.current_light_level <= 200:
                self.light_level_increasing = True

        # Update the light level display in the GreenhouseApp
        self.greenhouse_app.ids.light_level_card.value = f"{self.current_light_level:.0f} lux"

    def simulate_soil_moisture(self, dt):
        """
        Simulate the soil moisture fluctuating between 20% and 40%.
        """
        if self.soil_moisture_increasing:
            self.current_soil_moisture += 0.01
            if self.current_soil_moisture >= 0.40:
                self.soil_moisture_increasing = False
        else:
            self.current_soil_moisture -= 0.01
            if self.current_soil_moisture <= 0.20:
                self.soil_moisture_increasing = True

        # Update the soil moisture display in the GreenhouseApp
        self.greenhouse_app.ids.soil_moisture_card.value = f"{self.current_soil_moisture:.0%}"

# Run the app
if __name__ == '__main__':
    MyApp().run()
