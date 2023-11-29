import os

# Define the path for the main directory on the desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
main_folder_path = os.path.join(desktop_path, 'im')

# Define the structure of folders and subfolders
folders_structure = {
    "Photo": ["Landscape", "Portrait", "Street", "Nature", "Wildlife", "Urban", 
              "Architectural",  "Event", 
              "Astro", "Underwater", "Micro", "BnW"],
    "Traditional Art": ["Paintings/Oil", "Paintings/Acrylic", "Paintings/Watercolor", "Paintings/Gouache",
                        "Drawings/Pencil", "Drawings/Charcoal", "Drawings/Ink",
                        "Printmaking",
                        "Sculpture/Stone", "Sculpture/Metal", "Sculpture/Wood",
                        "Textile Arts/Weaving", "Textile Arts/Embroidery",
                        "Ceramics"],
    "Digital Art": ["Digital Paintings", "Illustrations", "3D Models", "Pixel Art",
                    "Graphic Design"],
    "Educational": ["Diagrams/Scientific", "Diagrams/Technical", "Diagrams/Medical",
                    "Infographics", "Maps/Historical", "Maps/Geographical", "Maps/Thematic",
                    "Instructional Images/How-To Guides", "Instructional Images/Educational Charts",
                    "Scientific Imagery/Astronomy", "Scientific Imagery/Biology", "Scientific Imagery/Physics", "Scientific Imagery/Chemistry",
                    "Historical Documents", "Medical Illustrations", "Graphs and Charts", "Educational Posters"]
}

# Function to create directories
def create_directories(base_path, structure):
    for main_folder, subfolders in structure.items():
        # Create main folder
        main_folder_path = os.path.join(base_path, main_folder)
        os.makedirs(main_folder_path, exist_ok=True)

        # Create subfolders
        for subfolder in subfolders:
            subfolder_path = os.path.join(main_folder_path, subfolder)
            os.makedirs(subfolder_path, exist_ok=True)

# Create the main 'im' folder and subfolders
create_directories(main_folder_path, folders_structure)

print("Folders created successfully on your desktop.")