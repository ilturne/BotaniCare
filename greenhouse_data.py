# greenhouse_data.py
import random
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, ListProperty, NumericProperty

class GreenhouseData(EventDispatcher):
    """
    Holds all greenhouse data/state, now as Kivy properties so UI updates automatically.
    """

    # Default colors
    DEFAULT_ON_COLOR = [0.3, 0.6, 0.3, 1.0]
    DEFAULT_OFF_COLOR = [0.812, 0.008, 0.008, 0.8]

    # Boolean properties for fan, lighting, and water pump
    fan_status = BooleanProperty(False)
    lighting_status = BooleanProperty(False)
    water_pump_status = BooleanProperty(False)

    # Corresponding color properties
    fan_status_color = ListProperty(DEFAULT_OFF_COLOR)
    lighting_status_color = ListProperty(DEFAULT_OFF_COLOR)
    water_pump_status_color = ListProperty(DEFAULT_OFF_COLOR)

    # Environment variables (for example, numeric properties):
    current_temperature = NumericProperty(75.0)
    current_humidity = NumericProperty(0.5)
    current_light_level = NumericProperty(300.0)
    current_soil_moisture = NumericProperty(0.3)

    # Some internal flags to simulate up/down cycles
    temperature_increasing = True
    humidity_increasing = True
    light_level_increasing = True
    soil_moisture_increasing = True

    # Thresholds (still normal dicts, used for ring color logic if needed)
    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize any additional logic you want here
        # ------------------ Plant Home Data ------------------
        self.user_name = "Ilya"
        self.healthy_species = 0
        self.total_species = 0
        self.title_text = f"Hello {self.user_name} you have {self.healthy_species}/{self.total_species} Healthy Species"

    # ------------------ Toggling Methods ------------------
    def toggle_fan_status(self):
        self.fan_status = not self.fan_status
        self.fan_status_color = (self.DEFAULT_ON_COLOR
                                 if self.fan_status
                                 else self.DEFAULT_OFF_COLOR)

    def toggle_lighting_status(self):
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = (self.DEFAULT_ON_COLOR
                                      if self.lighting_status
                                      else self.DEFAULT_OFF_COLOR)

    def toggle_water_pump_status(self):
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = (self.DEFAULT_ON_COLOR
                                        if self.water_pump_status
                                        else self.DEFAULT_OFF_COLOR)

    # -------------- Simulation Methods --------------
    def simulate_temperature(self):
        step = 0.1
        if self.temperature_increasing:
            self.current_temperature += step
            if self.current_temperature >= 80.0:
                self.temperature_increasing = False
        else:
            self.current_temperature -= step
            if self.current_temperature <= 75.0:
                self.temperature_increasing = True

    def simulate_humidity(self):
        # For demonstration
        self.current_humidity = random.uniform(0.40, 0.90)

    def simulate_light_level(self):
        step = 10
        if self.light_level_increasing:
            self.current_light_level += step
            if self.current_light_level >= 800:
                self.light_level_increasing = False
        else:
            self.current_light_level -= step
            if self.current_light_level <= 200:
                self.light_level_increasing = True

    def simulate_soil_moisture(self):
        step = 0.01
        if self.soil_moisture_increasing:
            self.current_soil_moisture += step
            if self.current_soil_moisture >= 0.60:
                self.soil_moisture_increasing = False
        else:
            self.current_soil_moisture -= step
            if self.current_soil_moisture <= 0.20:
                self.soil_moisture_increasing = True

    # (Optional) If you still want to evaluate ring color for your "cards",
    # keep the logic here:
    def evaluate_ring_color(self, value, thresholds):
        good_min, good_max = thresholds["good"]
        warn_min, warn_max = thresholds["warning"]
        if good_min <= value <= good_max:
            return [0.3, 0.6, 0.3, 0.8]  # Green
        elif warn_min <= value <= warn_max:
            return [1.0, 0.373, 0.082, 0.8]  # Orange
        else:
            return [0.812, 0.008, 0.008, 0.8]  # Red
