# screens/plant_home.py
from kivy.uix.screenmanager import Screen

class PlantHomeScreen(Screen):
    def __init__(self, greenhouse_data=None, **kwargs):
        super().__init__(**kwargs)
        self.greenhouse_data = greenhouse_data

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        # Example usage
        if self.greenhouse_data.user_name:
            title_text = (
                f"Hello {self.greenhouse_data.user_name} "
                f"you have {self.greenhouse_data.healthy_species}/"
                f"{self.greenhouse_data.total_species} Healthy Species"
            )
        else:
            title_text = (
                f"Hello you have {self.greenhouse_data.healthy_species}/"
                f"{self.greenhouse_data.total_species} Healthy Species"
            )
        # Possibly set some label's text to title_text, etc.
    
    def sort_by(self, criteria):
        print(f"Sorting by {criteria}")
        # After sorting, refresh the RecycleView
