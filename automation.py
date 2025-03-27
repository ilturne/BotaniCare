from datetime import datetime, timedelta
from greenhouse_data import GreenhouseData

SUNLIGHT_BRIGHTNESS = {
    "Full sun": 100,        # percent
    "part sun": 75,       # percent
    "Filtered shade": 25,   # percent
    "part shade": 50,     # percent
}

class GreenhouseController:
    def __init__(self, greenhouse_data: GreenhouseData):
        self.greenhouse_data = greenhouse_data
        self.last_watered = {}  # key: plant id, value: datetime
        self.last_brightness = None  # track the last set LED brightness

    def activate_fan(self):
        print("Fan activated.")
        # Insert code to control the fan actuator.
    
    def deactivate_fan(self):
        print("Fan deactivated.")
        # Insert code to control the fan actuator.
    
    def activate_water_pump(self, duration_seconds: int):
        print(f"Water pump activated for {duration_seconds} seconds.")
        # Insert code to control the water pump.
    
    def set_led_brightness(self, brightness_percent: int):
        # Only update if the brightness has changed
        if self.last_brightness != brightness_percent:
            print(f"Setting LED brightness to {brightness_percent}%.")
            # Insert code to control LED lights.
            self.last_brightness = brightness_percent
        else:
            print("LED brightness remains unchanged.")
    
    def check_temperature(self):
        current_temp = self.greenhouse_data.current_temperature
        target_max = self.greenhouse_data.get_global_temperature_max()  # Example function
        if current_temp > target_max:
            self.activate_fan()
        else:
            self.deactivate_fan()
    
    def check_watering(self):
        # Loop over each plant to determine if watering is due.
        for plant in self.greenhouse_data.user_added_plants:
            benchmark = plant.get('watering_general_benchmark', "{}")
            print(benchmark)
            try:
                import ast
                benchmark_dict = ast.literal_eval(benchmark)
                freq_range = benchmark_dict.get('value', '0-0')
                lower_bound = int(freq_range.split('-')[0])
            except Exception as e:
                lower_bound = 7  # Default to 7 days if error
            
            plant_id = plant.get('id')
            last_watered = self.last_watered.get(plant_id, None)
            now = datetime.now()
            if last_watered is None or now - last_watered > timedelta(days=lower_bound):
                depth_req_str = plant.get('depth_water_requirement', "{}")
                try:
                    depth_dict = ast.literal_eval(depth_req_str)
                    required_depth = int(depth_dict.get('value', 2))
                except Exception as e:
                    required_depth = 2  # default if not provided
                self.activate_water_pump(duration_seconds=5)
                self.last_watered[plant_id] = now
    
    def check_light(self):
        # Get the current hour (24-hour format)
        current_hour = datetime.now().hour
        # Define daytime as 6 AM (06:00) to 6 PM (18:00)
        if 6 <= current_hour < 18:
            # Daytime: set brightness based on plant's sunlight preference
            if self.greenhouse_data.user_added_plants:
                sunlight_str = self.greenhouse_data.user_added_plants[0].get('sunlight', 'Full sun')
                brightness = SUNLIGHT_BRIGHTNESS.get(sunlight_str, 100)
            else:
                brightness = 75  # Default if no plant data
        else:
            # Nighttime: set LED brightness to 0 (or a low value if you prefer dim light)
            brightness = 0
        self.set_led_brightness(brightness)
