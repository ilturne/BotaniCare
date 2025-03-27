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

# Automation Logic File
from automation import GreenhouseController

# Screens
from screens.home_screen import HomeScreen
from screens.plant_home import PlantHomeScreen
from screens.settings_screen import SettingsScreen

# Load KV files
Builder.load_file('kv/greenhouse.kv')
Builder.load_file('kv/plant_home.kv')
Builder.load_file('kv/settings.kv')

class MyApp(App):
    """
    Main application class.
    Creates and manages screens, schedules data updates, etc.
    """
    def build(self):
        # Create the shared greenhouse data
        self.greenhouse_data = GreenhouseData()
        self.greenhouse_controller = GreenhouseController(self.greenhouse_data)
        # ScreenManager setup
        self.sm = ScreenManager(transition=NoTransition())

        # Create & add home screen
        self.home_screen = HomeScreen(greenhouse_data=self.greenhouse_data, name='home')
        self.sm.add_widget(self.home_screen)

        # Create & add plant home screen
        self.plant_home_screen = PlantHomeScreen(greenhouse_data=self.greenhouse_data, name='PlantHome')
        self.sm.add_widget(self.plant_home_screen)

        # Create & add settings screen
        # Create & add settings screen
        self.settings_screen = SettingsScreen(greenhouse_data=self.greenhouse_data, name='settings')
        self.sm.add_widget(self.settings_screen)
        # Schedule simulation updates
        Clock.schedule_interval(self.update_environment, 2.0)

        # Start on the home screen
        self.sm.current = 'home'
        return self.sm

    def update_environment(self, dt):
        self.greenhouse_data.simulate_sensors()

        self.greenhouse_controller.check_temperature()
        self.greenhouse_controller.check_watering()
        self.greenhouse_controller.check_light()

        # self.greenhouse_data.get_humidity()
        # self.greenhouse_data.get_light_level()
        # self.greenhouse_data.get_temperature()
        # self.greenhouse_data.get_soil_moisture()
        
        self.home_screen.update_cards()
    
    def on_stop(self):
        self.greenhouse_data.save_state()
        

if __name__ == '__main__':
    MyApp().run()