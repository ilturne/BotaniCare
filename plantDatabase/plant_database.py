import os
import requests
import pandas as pd
import time

# Define your API key
API_KEY = 'sk-YvR1674ce443bfc8a7624'

# Base URLs for endpoints
base_list_url = "https://perenual.com/api/species-list"
base_detail_url = "https://perenual.com/api/species/details"

# List of 50 plant common names
plant_list = [
    "Spider Plant", "Snake Plant", "Peace Lily", "Pothos", "Philodendron",
    "Fiddle Leaf Fig", "ZZ Plant", "Boston Fern", "Aloe Vera", "Jade Plant",
    "Dracaena", "Monstera Deliciosa", "Rubber Plant", "Succulents", "Cacti",
    "African Violet", "Orchid", "Begonia", "Calathea", "Anthurium",
    "Prayer Plant", "Chinese Money Plant", "English Ivy", "Maidenhair Fern",
    "Basil", "Mint", "Rosemary", "Thyme", "Oregano", "Sage", "Parsley",
    "Chives", "Tomato", "Peppers", "Cucumbers", "Lettuce", "Spinach",
    "Strawberries", "Geraniums", "Petunias", "Marigolds", "Impatiens",
    "Pansies", "Florist Begonia", "Azalea", "Hydrangea", "Lilies",
    "Sunflowers", "Zinnias", "Gardenias"
]

# List to store detailed plant data
all_details = []

# Ensure the plantDatabase folder exists
os.makedirs("plantDatabase", exist_ok=True)

for plant in plant_list:
    print(f"Fetching data for {plant}...")
    # Step 1: Search for plant to get its ID
    list_params = {
        "key": API_KEY,
        "q": plant,
        "per_page": 1  # get the first matching species
    }
    list_response = requests.get(base_list_url, params=list_params)
    
    if list_response.status_code == 200:
        list_data = list_response.json().get("data", [])
        if list_data:
            plant_id = list_data[0].get("id")
            # Step 2: Fetch detailed information using the plant_id
            detail_params = {"key": API_KEY}
            detail_response = requests.get(f"{base_detail_url}/{plant_id}", params=detail_params)
            
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                # Add search term for reference
                detail_data["search_term"] = plant
                all_details.append(detail_data)
            else:
                print(f"Error fetching details for {plant} (ID: {plant_id}). Status: {detail_response.status_code}")
        else:
            print(f"No data found for {plant} in list search.")
    else:
        print(f"Error searching for {plant}. Status: {list_response.status_code}")
    
    # Delay to avoid rate limiting
    time.sleep(0.5)

# Step 3: Create DataFrame from collected data
df_all_details = pd.DataFrame(all_details)

# Step 4: Save the DataFrame to a CSV file
csv_path = os.path.join("plantDatabase", "detailed_plants_data.csv")
df_all_details.to_csv(csv_path, index=False)
print(f"Detailed data for all plants saved to {csv_path}")
