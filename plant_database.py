import pandas as pd

# Define the CSV file path for persistence
DB_FILE = "plant_database.csv"

# Define the default columns for the plant list
COLUMNS = ["Name", "Status", "Location", "Card"]

def initialize_database():
    """
    Initialize the plant database.
    If the CSV file does not exist, create it with default columns.
    """
    try:
        # Try to load the database
        return pd.read_csv(DB_FILE)
    except FileNotFoundError:
        # Create a new DataFrame if the file doesn't exist
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DB_FILE, index=False)
        return df

def add_plant(name, status, location, card):
    """
    Add a new plant to the database and save it to the CSV file.
    """
    df = initialize_database()
    new_plant = {"Name": name, "Status": status, "Location": location, "Card": card}
    df = df.append(new_plant, ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    return df

def get_plant_list():
    """
    Retrieve the list of plants from the database.
    """
    return initialize_database()
