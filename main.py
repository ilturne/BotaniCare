from kivy.config import Config

# Configure the window size for the Raspberry Pi touch screen or desktop usage
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

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
    A customizable status card displaying a title, a value, and a ring color indicator.
    Provides properties for background color, ring color, and font size of the displayed value.
    """
    value = StringProperty('--')
    ring_color = ListProperty([0.3, 0.6, 0.3, 0.8])  # Default ring color (green)
    bg_color = ListProperty([0.78, 0.85, 0.68, 0.9])  # Default background color
    value_font_size = NumericProperty(30)  # Default font size


class GreenhouseApp(FloatLayout):
    """
    Root layout of the Greenhouse application. Contains references to plant stats.
    """
    total_plants = NumericProperty(0)
    total_species = NumericProperty(0)
    available_spots = NumericProperty(0)


class MyApp(App):
    """
    Main application class. Handles data simulation and toggling of system states.
    Future Raspberry Pi GPIO integration or other hardware interaction can be added here.
    """
    # Default colors for system statuses (green = on, red = off, etc.)
    DEFAULT_ON_COLOR = [0.3, 0.6, 0.3, 1.0]
    DEFAULT_OFF_COLOR = [0.812, 0.008, 0.008, 0.8]

    # Status properties for fan, lighting, and water pump
    fan_status_color = ListProperty(DEFAULT_ON_COLOR)
    lighting_status_color = ListProperty(DEFAULT_ON_COLOR)
    water_pump_status_color = ListProperty(DEFAULT_ON_COLOR)
    fan_status = True
    lighting_status = True
    water_pump_status = True

    # Thresholds for evaluating ring color (these can be adjusted as needed)
    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

    def build(self):
        """
        Build the main application layout and initialize simulation variables.
        """
        self.greenhouse_app = GreenhouseApp()

        # Initialize environmental simulation values
        self.current_temperature = 75.0
        self.temperature_increasing = True

        self.current_humidity = 0.50
        self.humidity_increasing = True

        self.current_light_level = 300.0
        self.light_level_increasing = True

        self.current_soil_moisture = 0.30
        self.soil_moisture_increasing = True

        # Set initial plant data
        self.greenhouse_app.total_plants = 12
        self.greenhouse_app.total_species = 5
        self.greenhouse_app.available_spots = 3

        # Schedule simulation updates
        # For demonstration, updates occur every 0.2 seconds
        Clock.schedule_interval(self.simulate_temperature, 0.2)
        Clock.schedule_interval(self.simulate_humidity, 0.2)
        Clock.schedule_interval(self.simulate_light_level, 0.2)
        Clock.schedule_interval(self.simulate_soil_moisture, 0.2)

        return self.greenhouse_app

    def evaluate_ring_color(self, value, thresholds):
        """
        Evaluate ring color based on value thresholds.
        Returns green if within 'good' range, orange if warning, else red.
        """
        good_min, good_max = thresholds["good"]
        warn_min, warn_max = thresholds["warning"]

        if good_min <= value <= good_max:
            return [0.3, 0.6, 0.3, 0.8]  # Green
        elif warn_min <= value <= warn_max:
            return [1.0, 0.373, 0.082, 0.8]  # Orange
        else:
            return [0.812, 0.008, 0.008, 0.8]  # Red

    def toggle_fan_status(self):
        """
        Toggle the fan status and update the status light color.
        """
        self.fan_status = not self.fan_status
        self.fan_status_color = self.DEFAULT_ON_COLOR if self.fan_status else self.DEFAULT_OFF_COLOR

    def toggle_lighting_status(self):
        """
        Toggle the lighting status and update the status light color.
        """
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = self.DEFAULT_ON_COLOR if self.lighting_status else self.DEFAULT_OFF_COLOR

    def toggle_water_pump_status(self):
        """
        Toggle the water pump status and update the status light color.
        """
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = self.DEFAULT_ON_COLOR if self.water_pump_status else self.DEFAULT_OFF_COLOR

    def simulate_temperature(self, dt):
        """
        Simulate the temperature oscillating between 75°F and 80°F.
        """
        step = 0.1
        if self.temperature_increasing:
            self.current_temperature += step
            if self.current_temperature >= 80.0:
                self.temperature_increasing = False
        else:
            self.current_temperature -= step
            if self.current_temperature <= 75.0:
                self.temperature_increasing = True

        # Update UI
        self.update_card(
            card_id="temperature_card",
            value=f"{self.current_temperature:.1f}°F",
            thresholds=self.TEMPERATURE_THRESHOLDS,
            value_property=self.current_temperature
        )

    def simulate_humidity(self, dt):
        """
        Simulate random humidity between 40% and 90%.
        In a real scenario, this would be replaced with a sensor reading.
        """
        self.current_humidity = random.uniform(0.40, 0.90)
        self.update_card(
            card_id="humidity_card",
            value=f"{self.current_humidity:.0%}",
            thresholds=self.HUMIDITY_THRESHOLDS,
            value_property=self.current_humidity
        )

    def simulate_light_level(self, dt):
        """
        Simulate light level oscillating between 200 and 800 lux.
        """
        step = 10
        if self.light_level_increasing:
            self.current_light_level += step
            if self.current_light_level >= 800:
                self.light_level_increasing = False
        else:
            self.current_light_level -= step
            if self.current_light_level <= 200:
                self.light_level_increasing = True

        # Update UI
        self.update_card(
            card_id="light_level_card",
            value=f"{self.current_light_level:.0f} lux",
            thresholds=self.LIGHT_LEVEL_THRESHOLDS,
            value_property=self.current_light_level
        )

    def simulate_soil_moisture(self, dt):
        """
        Simulate soil moisture oscillating between 20% and 60%.
        """
        step = 0.01
        if self.soil_moisture_increasing:
            self.current_soil_moisture += step
            if self.current_soil_moisture >= 0.60:
                self.soil_moisture_increasing = False
        else:
            self.current_soil_moisture -= step
            if self.current_soil_moisture <= 0.20:
                self.soil_moisture_increasing = True

        # Update UI
        self.update_card(
            card_id="soil_moisture_card",
            value=f"{self.current_soil_moisture:.0%}",
            thresholds=self.SOIL_MOISTURE_THRESHOLDS,
            value_property=self.current_soil_moisture
        )

    def update_card(self, card_id, value, thresholds, value_property):
        """
        Helper method to update a card's displayed value and ring color.
        """
        card = self.greenhouse_app.ids.get(card_id)
        if card:
            card.value = value
            card.ring_color = self.evaluate_ring_color(value_property, thresholds)
        # If card doesn't exist, no action is taken (future: error handling/logging)


if __name__ == '__main__':
    MyApp().run()
