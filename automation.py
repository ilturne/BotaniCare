from datetime import datetime, timedelta
from greenhouse_data import GreenhouseData
import ActuatorTesting.Fan, ActuatorTesting.Pump, ActuatorTesting.Light
import lgpio
import time

SUNLIGHT_BRIGHTNESS = {
    "Full sun": 100,
    "part sun": 75,
    "Filtered shade": 25,
    "part shade": 50,
}

class GreenhouseController:
    """
    Controls fan, watering, and lighting based on greenhouse data.
    Throttles checks to conserve power: frequent during day, infrequent at night.
    """
    # Daytime window (inclusive start, exclusive end)
    DAY_START = 6
    DAY_END = 18
    # Intervals for checks
    DAY_CHECK_INTERVAL = timedelta(minutes=2)
    NIGHT_CHECK_INTERVAL = timedelta(hours=1)

    def __init__(self, greenhouse_data: GreenhouseData):
        self.data = greenhouse_data
        # Track last execution times per check
        self.last_temp_check = None
        self.last_watering_check = None
        self.last_light_check = None
        # Track last watered times per plant
        self.last_watered = {}
        # Track last LED brightness
        self.last_brightness = None

    def _should_run(self, last_run: datetime) -> bool:
        """
        Determine if a check should run based on current time and last_run.
        """
        now = datetime.now()
        # Choose interval
        if self.DAY_START <= now.hour < self.DAY_END:
            interval = self.DAY_CHECK_INTERVAL
        else:
            interval = self.NIGHT_CHECK_INTERVAL
        return (last_run is None) or (now - last_run >= interval)

    def activate_fan(self):
        print("Fan activated.")
        FAN_RELAY_PIN = 27
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, FAN_RELAY_PIN)
        ActuatorTesting.Fan.toggle_fan(h, FAN_RELAY_PIN, True)
        time.sleep(15)
        ActuatorTesting.Fan.toggle_fan(h, FAN_RELAY_PIN, False)
        lgpio.gpiochip_close(h)

    def deactivate_fan(self):
        print("Fan deactivated.")
        

    def activate_water_pump(self, duration_seconds: int):
        print(f"Water pump activated for {duration_seconds}s.")
        PUMP_CTRL_PIN = 22
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, PUMP_CTRL_PIN)
        ActuatorTesting.Pump.toggle_pump(h, PUMP_CTRL_PIN, True)
        time.sleep(1)
        ActuatorTesting.Pump.toggle_pump(h, PUMP_CTRL_PIN, False)
        lgpio.gpiochip_close(h)

    def set_led_brightness(self, brightness: int):
        # if self.last_brightness != brightness:
        #     print(f"LED brightness set to {brightness}%.")
        #     self.last_brightness = brightness
        LIGHT_RELAY_PIN = 17
        h = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_output(h, LIGHT_RELAY_PIN)
        ActuatorTesting.Light.toggle_light(h, LIGHT_RELAY_PIN, True)
        time.sleep(4)
        ActuatorTesting.Light.toggle_light(h, LIGHT_RELAY_PIN, False)
        lgpio.gpiochip_close(h)

    def check_temperature(self):
        if not self._should_run(self.last_temp_check):
            return
        now = datetime.now()
        temp = self.data.current_temperature
        # Use lowest max tolerance across plants
        max_allowed = self.data.get_global_temperature_max()
        if temp > max_allowed:
            #self.activate_fan()
            self.deactivate_fan()
        else:
            self.deactivate_fan()
        self.last_temp_check = now

    def check_watering(self):
        if not self._should_run(self.last_watering_check):
            return
        now = datetime.now()
        for plant in self.data.user_added_plants:
            plant_id = plant.get('id')
            # Determine watering frequency (days)
            try:
                import ast
                b = ast.literal_eval(plant.get('watering_general_benchmark', '{}'))
                days = int(b.get('value', '7').split('-')[0])
            except Exception:
                days = 7
            last = self.last_watered.get(plant_id)
            if (last is None) or (now - last > timedelta(days=days)):
                # Determine depth (default seconds)
                try:
                    d = ast.literal_eval(plant.get('depth_water_requirement', '{}'))
                    sec = int(d.get('value', 5))
                except Exception:
                    sec = 5
                #self.activate_water_pump(duration_seconds=sec)
                self.last_watered[plant_id] = now
        self.last_watering_check = now

    def check_light(self):
        if not self._should_run(self.last_light_check):
            return
        now = datetime.now()
        # Daytime brightness
        if self.DAY_START <= now.hour < self.DAY_END:
            if self.data.user_added_plants:
                pref = self.data.user_added_plants[0].get('sunlight', 'Full sun')
                brightness = SUNLIGHT_BRIGHTNESS.get(pref, 100)
            else:
                brightness = 75
        else:
            brightness = 0
        #self.set_led_brightness(brightness)
        self.last_light_check = now