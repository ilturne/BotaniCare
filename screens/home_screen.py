# screens/home_screen.py
from kivy.uix.screenmanager import Screen
from widgets.greenhouse_app import GreenhouseApp

class HomeScreen(Screen):
    """
    The 'main/home' screen that displays the GreenhouseApp layout.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create an instance of GreenhouseApp and add it to this Screen
        self.greenhouse_app = GreenhouseApp()
        self.add_widget(self.greenhouse_app)

    def on_pre_enter(self, *args):
        """
        Runs just before entering the screen.
        Useful for refreshing data if needed.
        """
        super().on_pre_enter(*args)
        # Example: print("Entering Home Screen")
