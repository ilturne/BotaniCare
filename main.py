from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

import os
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, NoTransition

# Shared Greenhouse Data
from greenhouse_data import GreenhouseData
# Screens
from screens.home_screen import HomeScreen
from screens.plant_home import PlantHomeScreen

# Load KV files
Builder.load_file('kv/greenhouse.kv')
Builder.load_file('kv/plant_home.kv')

class MyApp(App):
    """
    Main application class.
    Creates and manages screens, schedules data updates, etc.
    """

    def build(self):
        # Create the shared greenhouse data
        self.greenhouse_data = GreenhouseData()

        # ScreenManager setup
        self.sm = ScreenManager(transition=NoTransition())

        # Create & add home screen
        self.home_screen = HomeScreen(greenhouse_data=self.greenhouse_data, name='home')
        self.sm.add_widget(self.home_screen)

        # Create & add plant home screen
        self.plant_home_screen = PlantHomeScreen(greenhouse_data=self.greenhouse_data, name='PlantHome')
        self.sm.add_widget(self.plant_home_screen)

        # Schedule simulation updates
        Clock.schedule_interval(self.update_environment, 1.0)

        # Start on the home screen
        self.sm.current = 'home'
        return self.sm

    def update_environment(self, dt):
        # ... existing environment simulation code ...
        self.greenhouse_data.simulate_temperature()
        self.greenhouse_data.simulate_humidity()
        self.greenhouse_data.simulate_light_level()
        self.greenhouse_data.simulate_soil_moisture()

        self.home_screen.update_cards()

if __name__ == '__main__':
    MyApp().run()
