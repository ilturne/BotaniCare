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
    total_plants = NumericProperty(0)
    total_species = NumericProperty(0)
    available_spots = NumericProperty(0)

class MyApp(App):
    """
    The main application class that builds and runs the app.
    """
    fan_status_color = ListProperty([0.3, 0.6, 0.3, 1.0])  # Default to green (on)
    lighting_status_color = ListProperty([0.3, 0.6, 0.3, 1.0])  # Default to green (on)
    water_pump_status_color = ListProperty([0.3, 0.6, 0.3, 1.0])  # Default to green (on)
    fan_status = True
    lighting_status = True
    water_pump_status = True

    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

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

        self.greenhouse_app.total_plants = 12
        self.greenhouse_app.total_species = 5
        self.greenhouse_app.available_spots = 3

        # Schedule functions to simulate the environment
        Clock.schedule_interval(self.simulate_temperature, 0.2)
        Clock.schedule_interval(self.simulate_humidity, 0.2)
        Clock.schedule_interval(self.simulate_light_level, 0.2)
        Clock.schedule_interval(self.simulate_soil_moisture, 0.2)

        return self.greenhouse_app

    def evaluate_ring_color(self, value, thresholds): #Dynamically chgange the ring color based on valuels
        if thresholds["good"][0] <= value <= thresholds["good"][1]:
            return [0.3, 0.6, 0.3, 0.8]  # Green
        elif thresholds["warning"][0] <= value <= thresholds["warning"][1]:
            return [1.0, 0.373, 0.082, 0.8]  # Orange
        else:
            return [0.812, 0.008, 0.008, 0.8]  # Red

    def toggle_fan_status(self):
        """Toggle the fan status and update the status light."""
        self.fan_status = not self.fan_status
        self.fan_status_color = [0.3, 0.6, 0.3, 1.0] if self.fan_status else [0.812, 0.008, 0.008, 0.8]

    def toggle_lighting_status(self):
        """Toggle the lighting status and update the status light."""
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = [0.3, 0.6, 0.3, 1.0] if self.lighting_status else [0.812, 0.008, 0.008, 0.8]

    def toggle_water_pump_status(self):
        """Toggle the water pump status and update the status light."""
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = [0.3, 0.6, 0.3, 1.0] if self.water_pump_status else [0.812, 0.008, 0.008, 0.8]

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

        # Update the temperature display and ring color
        self.greenhouse_app.ids.temperature_card.value = f"{self.current_temperature:.1f}°F"
        self.greenhouse_app.ids.temperature_card.ring_color = self.evaluate_ring_color(
            self.current_temperature, self.TEMPERATURE_THRESHOLDS
        )

    def simulate_humidity(self, dt):
        """
        Simulate the humidity fluctuating between 40% and 90%.
        """
        self.current_humidity = random.uniform(0.40, 0.90)

        # Update the humidity display and ring color
        self.greenhouse_app.ids.humidity_card.value = f"{self.current_humidity:.0%}"
        self.greenhouse_app.ids.humidity_card.ring_color = self.evaluate_ring_color(
            self.current_humidity, self.HUMIDITY_THRESHOLDS
        )

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

        # Update the light level display and ring color
        self.greenhouse_app.ids.light_level_card.value = f"{self.current_light_level:.0f} lux"
        self.greenhouse_app.ids.light_level_card.ring_color = self.evaluate_ring_color(
            self.current_light_level, self.LIGHT_LEVEL_THRESHOLDS
        )

    def simulate_soil_moisture(self, dt):
        """
        Simulate the soil moisture fluctuating between 20% and 40%.
        """
        if self.soil_moisture_increasing:
            self.current_soil_moisture += 0.01
            if self.current_soil_moisture >= 0.60:
                self.soil_moisture_increasing = False
        else:
            self.current_soil_moisture -= 0.01
            if self.current_soil_moisture <= 0.20:
                self.soil_moisture_increasing = True

        # Update the soil moisture display and ring color
        self.greenhouse_app.ids.soil_moisture_card.value = f"{self.current_soil_moisture:.0%}"
        self.greenhouse_app.ids.soil_moisture_card.ring_color = self.evaluate_ring_color(
            self.current_soil_moisture, self.SOIL_MOISTURE_THRESHOLDS
        )

# Run the app
if __name__ == '__main__':
    MyApp().run()
