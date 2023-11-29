import os
import pycountry

# Define the path for the main directory on the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
main_folder_path = os.path.join(desktop_path, 'im/Photo/Urban')

# Get a list of all countries
countries = [country.name for country in pycountry.countries]

# Function to create directories
def create_directories(base_path, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

# Create a folder for each country
create_directories(main_folder_path, countries)

print("Country folders created successfully on your desktop.")
