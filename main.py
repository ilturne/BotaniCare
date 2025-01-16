# main.py
from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import ListProperty
import random

from kivy.uix.screenmanager import ScreenManager, NoTransition

# Screens
from screens.home_screen import HomeScreen
from screens.plant_home import PlantHomeScreen

# Load KV files
Builder.load_file('kv/greenhouse.kv')
Builder.load_file('kv/plant_home.kv')

class MyApp(App):
    """
    Main application class.
    Holds global data and logic (fan, lighting, pump statuses, etc.).
    """

    DEFAULT_ON_COLOR = [0.3, 0.6, 0.3, 1.0]
    DEFAULT_OFF_COLOR = [0.812, 0.008, 0.008, 0.8]

    fan_status_color = ListProperty(DEFAULT_ON_COLOR)
    lighting_status_color = ListProperty(DEFAULT_ON_COLOR)
    water_pump_status_color = ListProperty(DEFAULT_ON_COLOR)
    fan_status = True
    lighting_status = True
    water_pump_status = True

    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

    def build(self):
        # ScreenManager setup
        self.sm = ScreenManager(transition=NoTransition())
        
        # Create & add home screen
        self.home_screen = HomeScreen(name='home')
        self.sm.add_widget(self.home_screen)

        # Create & add plant home screen
        self.plant_home_screen = PlantHomeScreen(name='PlantHome')
        self.sm.add_widget(self.plant_home_screen)

        # Initialize environment simulation
        self.current_temperature = 75.0
        self.temperature_increasing = True

        self.current_humidity = 0.50
        self.humidity_increasing = True

        self.current_light_level = 300.0
        self.light_level_increasing = True

        self.current_soil_moisture = 0.30
        self.soil_moisture_increasing = True

        # Set initial plant data in the greenhouse_app (on the home screen)
        # We can reference the greenhouse_app object:
        self.home_screen.greenhouse_app.total_plants = 12
        self.home_screen.greenhouse_app.total_species = 5
        self.home_screen.greenhouse_app.available_spots = 3

        # Schedule simulation updates
        Clock.schedule_interval(self.simulate_temperature, 0.2)
        Clock.schedule_interval(self.simulate_humidity, 0.2)
        Clock.schedule_interval(self.simulate_light_level, 0.2)
        Clock.schedule_interval(self.simulate_soil_moisture, 0.2)

        # Start on the home screen
        self.sm.current = 'home'
        return self.sm

    # Example method to get a reference to greenhouse_app more directly
    @property
    def greenhouse_app(self):
        # Access the greenhouse_app inside home_screen
        return self.home_screen.greenhouse_app

    # -------------- Simulation / Toggling Methods --------------

    def toggle_fan_status(self):
        self.fan_status = not self.fan_status
        self.fan_status_color = self.DEFAULT_ON_COLOR if self.fan_status else self.DEFAULT_OFF_COLOR

    def toggle_lighting_status(self):
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = self.DEFAULT_ON_COLOR if self.lighting_status else self.DEFAULT_OFF_COLOR

    def toggle_water_pump_status(self):
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = self.DEFAULT_ON_COLOR if self.water_pump_status else self.DEFAULT_OFF_COLOR

    def simulate_temperature(self, dt):
        step = 0.1
        if self.temperature_increasing:
            self.current_temperature += step
            if self.current_temperature >= 80.0:
                self.temperature_increasing = False
        else:
            self.current_temperature -= step
            if self.current_temperature <= 75.0:
                self.temperature_increasing = True

        # Example UI update:
        self.update_card(
            card_id="temperature_card",
            value=f"{self.current_temperature:.1f}°F",
            thresholds=self.TEMPERATURE_THRESHOLDS,
            value_property=self.current_temperature
        )

    def simulate_humidity(self, dt):
        self.current_humidity = random.uniform(0.40, 0.90)
        self.update_card(
            card_id="humidity_card",
            value=f"{self.current_humidity:.0%}",
            thresholds=self.HUMIDITY_THRESHOLDS,
            value_property=self.current_humidity
        )

    def simulate_light_level(self, dt):
        step = 10
        if self.light_level_increasing:
            self.current_light_level += step
            if self.current_light_level >= 800:
                self.light_level_increasing = False
        else:
            self.current_light_level -= step
            if self.current_light_level <= 200:
                self.light_level_increasing = True

        self.update_card(
            card_id="light_level_card",
            value=f"{self.current_light_level:.0f} lux",
            thresholds=self.LIGHT_LEVEL_THRESHOLDS,
            value_property=self.current_light_level
        )

    def simulate_soil_moisture(self, dt):
        step = 0.01
        if self.soil_moisture_increasing:
            self.current_soil_moisture += step
            if self.current_soil_moisture >= 0.60:
                self.soil_moisture_increasing = False
        else:
            self.current_soil_moisture -= step
            if self.current_soil_moisture <= 0.20:
                self.soil_moisture_increasing = True

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

if __name__ == '__main__':
    MyApp().run()
