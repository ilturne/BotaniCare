# greenhouse_data.py
import random
import os
import csv
from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, ListProperty, NumericProperty, StringProperty
import pandas as pd

class GreenhouseData(EventDispatcher):
    """
    Shared data class.
    Holds environment variables, the public plant database, and user-added plants.
    """
    greenhouse_name = StringProperty("Ilya")
    greenhouse_units = StringProperty("Celsius")
    layout_rows = NumericProperty(5)
    layout_cols = NumericProperty(5)
    greenhouse_location = StringProperty("")  # If you want location, too

    # Default toggle colors
    DEFAULT_ON_COLOR = [0.3, 0.6, 0.3, 1.0]
    DEFAULT_OFF_COLOR = [0.812, 0.008, 0.008, 0.8]

    # Toggle properties
    fan_status = BooleanProperty(False)
    lighting_status = BooleanProperty(False)
    water_pump_status = BooleanProperty(False)
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

    # Species properties (reactive)
    healthy_species = NumericProperty(0)
    total_species = NumericProperty(0)
    title_text = StringProperty("")

    # Thresholds
    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize user data and title text
        self.user_name = "Ilya"
        self.healthy_species = 0
        self.total_species = 0
        self._update_title_text()

        # Load the public and user-added plant databases
        self.plant_database = []
        self.load_plant_database()
        self.user_added_plants = []
        self.load_user_plants()

    def _update_title_text(self):
        # Update the reactive title_text property.
        self.title_text = f"Hello {self.greenhouse_name} you have {self.healthy_species}/{self.total_species} Healthy Species"

    def load_plant_database(self):
        """Load the public plant database from CSV."""
        csv_path = os.path.join("plantDatabase", "detailed_plants_data.csv")
        if not os.path.exists(csv_path):
            print(f"Warning: CSV not found at {csv_path}")
            return
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.plant_database = list(reader)
        print(f"Loaded {len(self.plant_database)} entries from {csv_path}")

    def load_user_plants(self):
        """Load the user-added plants from CSV."""
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        if os.path.exists(user_csv):
            df_user = pd.read_csv(user_csv)
            self.user_added_plants = df_user.to_dict(orient='records')
            # Assume all loaded plants are healthy.
            self.total_species = len(self.user_added_plants)
            self.healthy_species = len(self.user_added_plants)
            print(f"Loaded {len(self.user_added_plants)} user-added plants from {user_csv}")
        else:
            self.user_added_plants = []
            print(f"No user-added plants CSV found at {user_csv}. Starting empty.")
        self._update_title_text()

    def save_user_plants(self):
        """Save user-added plants to CSV (preserving headers if empty)."""
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        headers = [
            "id", "common_name", "scientific_name", "other_name", "family", "origin", "type",
            "dimension", "dimensions", "cycle", "attracts", "propagation", "hardiness",
            "hardiness_location", "watering", "depth_water_requirement", "volume_water_requirement",
            "watering_period", "watering_general_benchmark", "plant_anatomy", "sunlight",
            "pruning_month", "pruning_count", "seeds", "maintenance", "care-guides", "soil",
            "growth_rate", "drought_tolerant", "salt_tolerant", "thorny", "invasive", "tropical",
            "indoor", "care_level", "pest_susceptibility", "pest_susceptibility_api", "flowers",
            "flowering_season", "flower_color", "cones", "fruits", "edible_fruit",
            "edible_fruit_taste_profile", "fruit_nutritional_value", "fruit_color", "harvest_season",
            "leaf", "leaf_color", "edible_leaf", "cuisine", "medicinal", "poisonous_to_humans",
            "poisonous_to_pets", "description", "default_image", "other_images", "search_term"
        ]
        if not self.user_added_plants:
            df_user = pd.DataFrame(columns=headers)
        else:
            df_user = pd.DataFrame(self.user_added_plants)
        df_user.to_csv(user_csv, index=False)
        print(f"Saved {len(self.user_added_plants)} user-added plants to {user_csv}.")

    def add_user_plant(self, plant):
        """
        Adds a new plant (assumed healthy), updates counts & title, and saves.
        """
        self.user_added_plants.append(plant)
        self.healthy_species += 1
        self.total_species += 1
        self._update_title_text()
        self.save_user_plants()

    def remove_user_plant(self, plant_id):
        """
        Removes plant(s) by id, updates counts & title, and saves.
        """
        before_count = len(self.user_added_plants)
        self.user_added_plants = [p for p in self.user_added_plants if p.get('id') != plant_id]
        removed_count = before_count - len(self.user_added_plants)
        print(f"Removed {removed_count} user plants with ID={plant_id}.")
        if removed_count > 0:
            self.healthy_species = max(0, self.healthy_species - removed_count)
            self.total_species = max(0, self.total_species - removed_count)
        self._update_title_text()
        self.save_user_plants()

    # Toggle & simulation methods below...
    def toggle_fan_status(self):
        self.fan_status = not self.fan_status
        self.fan_status_color = self.DEFAULT_ON_COLOR if self.fan_status else self.DEFAULT_OFF_COLOR

    def toggle_lighting_status(self):
        self.lighting_status = not self.lighting_status
        self.lighting_status_color = self.DEFAULT_ON_COLOR if self.lighting_status else self.DEFAULT_OFF_COLOR

    def toggle_water_pump_status(self):
        self.water_pump_status = not self.water_pump_status
        self.water_pump_status_color = self.DEFAULT_ON_COLOR if self.water_pump_status else self.DEFAULT_OFF_COLOR

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
