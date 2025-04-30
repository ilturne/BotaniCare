# greenhouse_data.py
import json
import random
import os
import csv
import pandas as pd
import lgpio
import time
import ActuatorTesting.Fan
from kivy.event import EventDispatcher
from kivy.properties import (
    BooleanProperty, ListProperty, NumericProperty, StringProperty
)

#Sensor Files Linux Only!
import SensorTesting.DHT20, SensorTesting.Grove, SensorTesting.SFH213FA

#temperature sensor data
from w1thermsensor import W1ThermSensor

HARDINESS_TEMPERATURE_TABLE = {
    1:  (-60, -50),
    2:  (-50, -40),
    3:  (-40, -30),
    4:  (-30, -20),
    5:  (-20, -10),
    6:  (-10,   0),
    7:  (  0,  10),
    8:  ( 10,  20),
    9:  ( 20,  30),
    10: ( 30,  40),
    11: ( 40,  50),
    12: ( 50,  60),
    13: ( 60,  70),
}

FAN = 0
PUMP = 0
LIGHT = 0

class GreenhouseData(EventDispatcher):
    # File where the state is saved
    STATE_FILE = "state.json"
    
    # Shared settings (centralized data)
    greenhouse_name = StringProperty("")
    greenhouse_units = StringProperty("Imperial")
    layout_rows = NumericProperty(0)
    layout_cols = NumericProperty(0)

    # Plant-related properties
    total_plants = NumericProperty(0)
    healthy_species = NumericProperty(0)
    total_species = NumericProperty(0)
    title_text = StringProperty("")
    available_spots = NumericProperty(0)
    
    # Default colors for toggles
    DEFAULT_ON_COLOR = [0.3, 0.6, 0.3, 1.0]
    DEFAULT_OFF_COLOR = [0.812, 0.008, 0.008, 0.8]
    
    # Toggle statuses & colors
    fan_status = BooleanProperty(False)
    lighting_status = BooleanProperty(False)
    water_pump_status = BooleanProperty(False)
    fan_status_color = ListProperty(DEFAULT_OFF_COLOR)
    lighting_status_color = ListProperty(DEFAULT_OFF_COLOR)
    water_pump_status_color = ListProperty(DEFAULT_OFF_COLOR)
    
    # Environment variables
    current_temperature = NumericProperty(0)
    current_humidity = NumericProperty(0)
    current_light_level = NumericProperty(0)
    current_soil_moisture = NumericProperty(0)
    temperature_increasing = True
    humidity_increasing = True
    light_level_increasing = True
    soil_moisture_increasing = True

    #sensor variables
    temperatureSensor = W1ThermSensor()

    # Thresholds for evaluating ring colors (for UI feedback)
    TEMPERATURE_THRESHOLDS = {"good": (64, 75), "warning": (50, 85)}
    HUMIDITY_THRESHOLDS = {"good": (0.5, 0.7), "warning": (0.4, 0.8)}
    SOIL_MOISTURE_THRESHOLDS = {"good": (0.2, 0.4), "warning": (0.1, 0.5)}
    LIGHT_LEVEL_THRESHOLDS = {"good": (200, 800), "warning": (100, 1000)}
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize counts and title text
        self.load_state()  # uses default STATE_FILE
    
        # Load plant data and user plants
        self.plant_database = []
        self.load_plant_database()
        self.user_added_plants = []
        self.update_available_spots()
        self.load_user_plants()
    

    def _update_title_text(self):
        """Update the reactive title text used in the UI."""
        self.title_text = (
            f"Hello {self.greenhouse_name} you have "
            f"{self.healthy_species}/{self.total_species} Healthy Species"
        )
    def update_available_spots(self):
        self.available_spots = (self.layout_rows * self.layout_cols) - self.total_plants 

    def load_plant_database(self):
        """Load the public plant database from a CSV file."""
        csv_path = os.path.join("plantDatabase", "detailed_plants_data.csv")
        if not os.path.exists(csv_path):
            print(f"Warning: CSV not found at {csv_path}")
            return
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.plant_database = list(reader)
        print(f"Loaded {len(self.plant_database)} entries from {csv_path}")
    
    def load_user_plants(self):
        """Load the user-added plants from a CSV file."""
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        if os.path.exists(user_csv):
            df_user = pd.read_csv(user_csv)
            self.user_added_plants = df_user.to_dict(orient="records")
            self.total_species = len(self.user_added_plants)
            self.total_plants = len(self.user_added_plants)
            self.healthy_species = len(self.user_added_plants)
            print(f"Loaded {len(self.user_added_plants)} user-added plants from {user_csv}")
        else:
            self.user_added_plants = []
            print(f"No user-added plants CSV found at {user_csv}. Starting empty.")
        self._update_title_text()
    
    def save_user_plants(self):
        """Save user-added plants to a CSV file."""
        user_csv = os.path.join("plantDatabase", "user_added_plants.csv")
        headers = [
            "id", "common_name", "scientific_name", "other_name", "family",
            "origin", "type", "dimension", "dimensions", "cycle", "attracts",
            "propagation", "hardiness", "hardiness_location", "watering",
            "depth_water_requirement", "volume_water_requirement",
            "watering_period", "watering_general_benchmark", "plant_anatomy",
            "sunlight", "pruning_month", "pruning_count", "seeds", "maintenance",
            "care-guides", "soil", "growth_rate", "drought_tolerant",
            "salt_tolerant", "thorny", "invasive", "tropical", "indoor",
            "care_level", "pest_susceptibility", "pest_susceptibility_api",
            "flowers", "flowering_season", "flower_color", "cones", "fruits",
            "edible_fruit", "edible_fruit_taste_profile", "fruit_nutritional_value",
            "fruit_color", "harvest_season", "leaf", "leaf_color", "edible_leaf",
            "cuisine", "medicinal", "poisonous_to_humans", "poisonous_to_pets",
            "description", "default_image", "other_images", "search_term", "temperature_min", "temperature_max"
        ]
        if not self.user_added_plants:
            df_user = pd.DataFrame(columns=headers)
        else:
            df_user = pd.DataFrame(self.user_added_plants)
        df_user.to_csv(user_csv, index=False)
        print(f"Saved {len(self.user_added_plants)} user-added plants to {user_csv}.")
    
    def get_hardiness_temp_range(zone: int) -> tuple[float, float]:
        return HARDINESS_TEMPERATURE_TABLE.get(zone, (None, None))

    def add_user_plant(self, plant):
        """Add a new plant, update counts, and save."""
        self.user_added_plants.append(plant)
        self.healthy_species += 1
        self.total_species += 1
        self._update_title_text()
        self.save_user_plants()
    
    def remove_user_plant(self, plant_id):
        before_count = len(self.user_added_plants)
        self.user_added_plants = [
            p for p in self.user_added_plants if str(p.get("id")) != str(plant_id)
        ]
        removed_count = before_count - len(self.user_added_plants)
        print(f"Removed {removed_count} user plants with ID={plant_id}.")
        if removed_count > 0:
            self.healthy_species = max(0, self.healthy_species - removed_count)
            self.total_species = max(0, self.total_species - removed_count)
        self._update_title_text()
        self.save_user_plants()
    
    # Toggle methods for hardware simulation
    def toggle_fan_status(self):
        global FAN
        FAN_RELAY_PIN = 27
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, FAN_RELAY_PIN)
        if (FAN == 0):
            ActuatorTesting.Fan.toggle_fan(h, FAN_RELAY_PIN, True)
            FAN = 1
            lgpio.gpiochip_close(h)
            self.fan_status = not self.fan_status
            self.fan_status_color = self.DEFAULT_ON_COLOR
        elif (FAN == 1):
            ActuatorTesting.Fan.toggle_fan(h, FAN_RELAY_PIN, False)
            FAN = 0
            lgpio.gpiochip_close(h)
            self.fan_status = not self.fan_status
            self.fan_status_color = self.DEFAULT_OFF_COLOR
        
    
    def toggle_lighting_status(self):
        global LIGHT
        LIGHT_RELAY_PIN = 17
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, LIGHT_RELAY_PIN)
        if (LIGHT == 0):
            ActuatorTesting.Light.toggle_light(h, LIGHT_RELAY_PIN, True)
            LIGHT = 1
            lgpio.gpiochip_close(h)
            self.lighting_status = not self.lighting_status
            self.lighting_status_color = self.DEFAULT_ON_COLOR
        elif (LIGHT == 1):
            ActuatorTesting.Light.toggle_light(h, LIGHT_RELAY_PIN, False)
            LIGHT = 0
            lgpio.gpiochip_close(h)
            self.lighting_status = not self.lighting_status
            self.lighting_status_color = self.DEFAULT_OFF_COLOR
        # self.lighting_status = not self.lighting_status
        # self.lighting_status_color = self.DEFAULT_ON_COLOR if self.lighting_status else self.DEFAULT_OFF_COLOR
    
    def toggle_water_pump_status(self):
        global PUMP
        PUMP_RELAY_PIN = 22
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, PUMP_RELAY_PIN)
        if (PUMP == 0):
            ActuatorTesting.Pump.toggle_pump(h, PUMP_RELAY_PIN, True)
            PUMP = 1
            lgpio.gpiochip_close(h)
            self.water_pump_status = not self.water_pump_status
            self.water_pump_status_color = self.DEFAULT_ON_COLOR
        elif (PUMP == 1):
            ActuatorTesting.Pump.toggle_pump(h, PUMP_RELAY_PIN, False)
            PUMP = 0
            lgpio.gpiochip_close(h)
            self.water_pump_status = not self.water_pump_status
            self.water_pump_status_color = self.DEFAULT_OFF_COLOR

    # def simulate_sensors(self):
    #     #Temperature Sensor
    #     step = 0.1
    #     if self.temperature_increasing:
    #         self.current_temperature += step
    #         if self.current_temperature >= 80.0:
    #             self.temperature_increasing = False
    #     else:
    #         self.current_temperature -= step
    #         if self.current_temperature <= 75.0:
    #             self.temperature_increasing = True

    #     #Humidity Sensor
    #     self.current_humidity = random.uniform(0.40, 0.90)
        
    #     Light Sensor
    #     if self.light_level_increasing:
    #         self.current_light_level += step
    #         if self.current_light_level >= 800:
    #             self.light_level_increasing = False
    #     else:
    #         self.current_light_level -= step
    #         if self.current_light_level <= 200:
    #             self.light_level_increasing = True
        
    #     Soil Moisture Sensor
    #     if self.soil_moisture_increasing:
    #         self.current_soil_moisture += step
    #         if self.current_soil_moisture >= 0.60:
    #             self.soil_moisture_increasing = False
    #     else:
    #         self.current_soil_moisture -= step
    #         if self.current_soil_moisture <= 0.20:
    #             self.soil_moisture_increasing = True
    
    def evaluate_ring_color(self, value, thresholds):
        good_min, good_max = thresholds["good"]
        warn_min, warn_max = thresholds["warning"]
        if good_min <= value <= good_max:
            return [0.3, 0.6, 0.3, 0.8]
        elif warn_min <= value <= warn_max:
            return [1.0, 0.373, 0.082, 0.8]
        else:
            return [0.812, 0.008, 0.008, 0.8]
    
    # Uncomment when usign the Pi
    def get_temperature(self):
        if self.greenhouse_units == "Imperial":
            try:
                self.current_temperature = (((self.temperatureSensor.get_temperature()) * 1.8) + 32)
            except Exception as e:
                print("Temperature sensor error:", e)
                self.current_temperature = 0
        else: 
            try:
                self.current_temperature = self.temperatureSensor.get_temperature()
            except Exception as e:
                print("Temperature sensor error:", e)
                self.current_temperature = 0

    # #This is Linux only so when on the Pi uncomment this
    def get_light_level(self):
        try:
            adc_value = SensorTesting.SFH213FA.read_adc(0)
            voltage = SensorTesting.SFH213FA.adc_to_voltage(adc_value)
            light_intensity = SensorTesting.SFH213FA.voltage_to_light_intensity(voltage)
            self.current_light_level = light_intensity
        except Exception as e:
            print("Light sensor error:", e)
            self.current_light_level = 0

    def get_humidity(self):
        try:
            DHT20_I2C_BUS = 1
            DHT20_I2C_ADDR = 0x38
            dht20 = SensorTesting.DHT20.DFRobot_DHT20(DHT20_I2C_BUS, DHT20_I2C_ADDR)
            temp, hum = dht20.get_temperature_and_humidity()
            self.current_humidity = hum * .01
        except Exception as e:
            print("Humidity sensor error:", e)
            self.current_humidity = 0

    # #This is Linux only so when on the Pi uncomment this
    def get_soil_moisture(self):
        try:
            adc_value = SensorTesting.Grove.read_adc(1)
            voltage = SensorTesting.Grove.adc_to_voltage(adc_value)
            moisture_percentage = SensorTesting.Grove.voltage_to_moisture(voltage)
            self.current_soil_moisture = moisture_percentage * .01
        except Exception as e:
            print("Soil moisture sensor error:", e)
            self.current_soil_moisture = 0

    # Save and load state methods
    def save_state(self, state_file: str = None):
        """Save shared settings and environment variables to a JSON file."""
        if state_file is None:
            state_file = self.STATE_FILE
        state = {
            "greenhouse_name": self.greenhouse_name,
            "greenhouse_units": self.greenhouse_units,
            "layout_rows": self.layout_rows,
            "layout_cols": self.layout_cols,
            "available_spots": self.available_spots,
            "current_temperature": self.current_temperature,
            "current_humidity": self.current_humidity,
            "current_light_level": self.current_light_level,
            "current_soil_moisture": self.current_soil_moisture,
            "fan_status": self.fan_status,
            "lighting_status": self.lighting_status,
            "water_pump_status": self.water_pump_status,
            "total_plants": self.total_plants,
            "healthy_species": self.healthy_species,
            "total_species": self.total_species,
        }
        try:
            with open(state_file, "w") as f:
                json.dump(state, f)
            print(f"State saved to {state_file}.")
        except Exception as e:
            print("Error saving state:", e)
    
    def get_global_temperature_max(self):
        lowest_max = None
        for plant in self.user_added_plants:
            temp_max_value = plant.get("temperature_max")
            if temp_max_value is None:
                continue
            try:
                temp_max = float(temp_max_value)
            except ValueError:
                continue
            if lowest_max is None or temp_max < lowest_max:
                lowest_max = temp_max
        return lowest_max if lowest_max is not None else 0
    
    def load_state(self, state_file: str = None):
        """Load shared settings and environment variables from a JSON file."""
        if state_file is None:
            state_file = self.STATE_FILE
        if not os.path.exists(state_file):
            print("No previous state file found.")
            return
        try:
            with open(state_file, "r") as f:
                state = json.load(f)
            self.greenhouse_name = state.get("greenhouse_name", self.greenhouse_name)
            self.greenhouse_units = state.get("greenhouse_units", self.greenhouse_units)
            self.layout_rows = state.get("layout_rows", self.layout_rows)
            self.layout_cols = state.get("layout_cols", self.layout_cols)
            self.available_spots = state.get("available_spots", self.available_spots)
            self.current_temperature = state.get("current_temperature", self.current_temperature)
            self.current_humidity = state.get("current_humidity", self.current_humidity)
            self.current_light_level = state.get("current_light_level", self.current_light_level)
            self.current_soil_moisture = state.get("current_soil_moisture", self.current_soil_moisture)
            self.fan_status = state.get("fan_status", self.fan_status)
            self.lighting_status = state.get("lighting_status", self.lighting_status)
            self.water_pump_status = state.get("water_pump_status", self.water_pump_status)
            self.total_plants = state.get("total_plants", self.total_plants)
            self.healthy_species = state.get("healthy_species", self.healthy_species)
            self.total_species = state.get("total_species", self.total_species)
            self._update_title_text()
            print(f"State loaded from {state_file}.")
        except Exception as e:
            print("Error loading state:", e)