# screens/home_screen.py
from kivy.uix.screenmanager import Screen
from widgets.greenhouse_app import GreenhouseApp #This probably won't be necessary later but I don't know what to do with it right now

class HomeScreen(Screen):
    """
    The 'main/home' screen that displays the GreenhouseApp layout.
    """
    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data

        # Create an instance of GreenhouseApp and add it to this Screen
        self.greenhouse_app = GreenhouseApp()
        self.add_widget(self.greenhouse_app)

    def on_pre_enter(self, *args):
        """
        Runs just before entering the screen.
        Useful for refreshing data if needed.
        """
        super().on_pre_enter(*args)
        # Example: update your cards here:
        self.update_cards()

    def update_cards(self):
        """
        Grabs environment data from greenhouse_data, updates the UI cards.
        """
        if not self.greenhouse_data:
            return

        # Temperature card:
        self.update_card(
            card_id="temperature_card",
            value=f"{self.greenhouse_data.current_temperature:.1f}°F",
            thresholds=self.greenhouse_data.TEMPERATURE_THRESHOLDS,
            value_property=self.greenhouse_data.current_temperature,
        )

        # Humidity card:
        self.update_card(
            card_id="humidity_card",
            value=f"{self.greenhouse_data.current_humidity:.0%}",
            thresholds=self.greenhouse_data.HUMIDITY_THRESHOLDS,
            value_property=self.greenhouse_data.current_humidity,
        )

        # Light level card:
        self.update_card(
            card_id="light_level_card",
            value=f"{self.greenhouse_data.current_light_level:.0f} lux",
            thresholds=self.greenhouse_data.LIGHT_LEVEL_THRESHOLDS,
            value_property=self.greenhouse_data.current_light_level,
        )

        # Soil moisture card:
        self.update_card(
            card_id="soil_moisture_card",
            value=f"{self.greenhouse_data.current_soil_moisture:.0%}",
            thresholds=self.greenhouse_data.SOIL_MOISTURE_THRESHOLDS,
            value_property=self.greenhouse_data.current_soil_moisture,
        )

    def update_card(self, card_id, value, thresholds, value_property):
        """
        Helper method to update a card's displayed value and ring color.
        """
        card = self.greenhouse_app.ids.get(card_id)
        if card:
            card.value = value
            # Use greenhouse_data's evaluate_ring_color logic
            card.ring_color = self.greenhouse_data.evaluate_ring_color(value_property, thresholds)