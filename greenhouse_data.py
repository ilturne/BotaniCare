# greenhouse_data.py
import random
import os
import csv
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, ListProperty, NumericProperty
import pandas as pd

class GreenhouseData(EventDispatcher):
    """
    Holds all greenhouse data/state, including:
      - Environment variables / toggles
      - The main (public) plant database from detailed_plants_data.csv
      - The user-added plant database from user_added_plants.csv
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

    # Environment variables
    current_temperature = NumericProperty(75.0)
    current_humidity = NumericProperty(0.5)
    current_light_level = NumericProperty(300.0)
    current_soil_moisture = NumericProperty(0.3)

    # Simulation flags
    temperature_increasing = True
    humidity_increasing = True
    light_level_increasing = True
    soil_moisture_increasing = True

    # Thresholds
    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ------------------ Plant Home Data ------------------
        self.user_name = "Ilya"
        self.healthy_species = 0
        self.total_species = 0
        self.title_text = f"Hello {self.user_name} you have {self.healthy_species}/{self.total_species} Healthy Species"

        # ------------------ Main (Public) Plant Database ------------------
        # We'll store your CSV contents here as a list of dicts
        self.plant_database = []
        self.load_plant_database()

        # ------------------ User-Added Plant Database ------------------
        # A separate list of dicts for plants the user adds
        self.user_added_plants = []
        self.load_user_plants()

    # ------------------- PUBLIC PLANT DATABASE -------------------

    def load_plant_database(self):
        """
        Loads the main detailed_plants_data.csv into self.plant_database.
        These are the plants that come "pre-installed" in your system.
        """
        csv_path = os.path.join("plantDatabase", "detailed_plants_data.csv")
        if not os.path.exists(csv_path):
            print(f"Warning: CSV not found at {csv_path}")
            return

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.plant_database = list(reader)

        print(f"Loaded {len(self.plant_database)} entries from {csv_path}")

    # ------------------- USER-ADDED PLANT DATABASE -------------------
    def load_user_plants(self):
        """
        Loads user_added_plants.csv into self.user_added_plants.
        These are plants the user manually adds to the system.
        """
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        if os.path.exists(user_csv):
            df_user = pd.read_csv(user_csv)
            self.user_added_plants = df_user.to_dict(orient='records')
            print(f"Loaded {len(self.user_added_plants)} user-added plants from {user_csv}")
        else:
            self.user_added_plants = []
            print(f"No user-added plants CSV found at {user_csv}. Starting empty.")

    def save_user_plants(self):
        """
        Saves the current self.user_added_plants list to user_added_plants.csv.
        """
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        df_user = pd.DataFrame(self.user_added_plants)
        df_user.to_csv(user_csv, index=False)
        print(f"Saved {len(self.user_added_plants)} user-added plants to {user_csv}.")

    def add_user_plant(self, plant):
        """
        Adds a new plant dict to self.user_added_plants and writes to CSV.
        Example: plant = {'id': 1, 'common_name': 'Tomato', ...}
        """
        self.user_added_plants.append(plant)
        self.save_user_plants()

    def remove_user_plant(self, plant_id):
        """
        Removes a user plant by id from self.user_added_plants and saves to CSV.
        """
        before_count = len(self.user_added_plants)
        self.user_added_plants = [p for p in self.user_added_plants if p.get('id') != plant_id]
        after_count = len(self.user_added_plants)
        print(f"Removed {before_count - after_count} user plants with ID={plant_id}.")
        self.save_user_plants()

    # ------------------ Toggling Methods (Environment) ------------------
    def toggle_fan_status(self):
        self.fan_status = not self.fan_status
        self.fan_status_color = self.DEFAULT_ON_COLOR if self.fan_status else self.DEFAULT_OFF_COLOR

    def toggle_lighting_status(self):
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = self.DEFAULT_ON_COLOR if self.lighting_status else self.DEFAULT_OFF_COLOR

    def toggle_water_pump_status(self):
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = self.DEFAULT_ON_COLOR if self.water_pump_status else self.DEFAULT_OFF_COLOR

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

    def evaluate_ring_color(self, value, thresholds):
        good_min, good_max = thresholds["good"]
        warn_min, warn_max = thresholds["warning"]
        if good_min <= value <= good_max:
            return [0.3, 0.6, 0.3, 0.8]
        elif warn_min <= value <= warn_max:
            return [1.0, 0.373, 0.082, 0.8]
        else:
            return [0.812, 0.008, 0.008, 0.8]
