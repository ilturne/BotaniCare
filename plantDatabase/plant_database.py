import os
import requests
import pandas as pd
import time

# Define your API key
API_KEY = 'sk-YvR1674ce443bfc8a7624'

base_list_url = "https://perenual.com/api/species-list"
base_detail_url = "https://perenual.com/api/species/details"

plant_list = [
    
]
# Path to the CSV file where detailed plant data is stored
csv_path = os.path.join("plantDatabase", "detailed_plants_new_data.csv")

# Ensure the plantDatabase folder exists
os.makedirs("plantDatabase", exist_ok=True)

# Load existing plant data if available
existing_details = []

# Create a dictionary for quick lookup by common name from existing data
existing_by_name = {}
for detail in existing_details:
    # Use the search_term field if it was saved, or common_name directly
    key = detail.get("search_term") or detail.get("common_name")
    if key:
        existing_by_name[key.lower()] = detail

# List to store new detailed plant data
new_details = []

for plant in plant_list:
    # Check if plant data already exists to skip API call
    if plant.lower() in existing_by_name:
        print(f"Data for '{plant}' already exists. Skipping API request.")
        continue  # Skip to the next plant

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
                new_details.append(detail_data)
            else:
                print(f"Error fetching details for {plant} (ID: {plant_id}). Status: {detail_response.status_code}")
        else:
            print(f"No data found for {plant} in list search.")
    else:
        print(f"Error searching for {plant}. Status: {list_response.status_code}")

    # Delay to avoid rate limiting
    time.sleep(0.5)

# Combine existing details with new details
all_details = existing_details + new_details

# Step 3: Create DataFrame from combined data
df_all_details = pd.DataFrame(all_details)

# Step 4: Save the DataFrame to a CSV file (overwrite with updated info)
df_all_details.to_csv(csv_path, index=False)
print(f"Detailed data for all plants saved to {csv_path}")
