import requests
import time
import random
import os

artists = [
    "Robert Adam",
    "Aert van Tricht",
    "Ahmad ibn al-Suhrawardi",
    "Leon Battista Alberti",
    "Albrecht Altdorfer",
    "Amasis Painter",
    "John Frederick Amelung",
    "Rafael and Gaspar Amezúa",
    "Andokides Painter",
    "Andrea del Sarto",
    "Fra Angelico",
    "Pier Jacopo Alari Bonacolsi",
    "Antonio da Sangallo the Younger",
    "Arkesilas Painter",
    "Tiziano Aspetti",
    "Milton Avery",
    "Hans Baldung",
    "Edouard Baldus",
    "Balthus",
    "Baccio Bandinelli"
]

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def search_artworks_by_artist(artist_name):
    search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {
        'q': artist_name,
        'hasImages': True
    }
    try:
        response = requests.get(search_url, params=params)
        if response.status_code == 200:
            return response.json().get('objectIDs', [])
        else:
            return []  # Return an empty list if the response is not successful
    except requests.RequestException:
        return []  # Return an empty list in case of a request failure

def fetch_and_save_artwork_image(object_id, artist_name):
    details_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    response = requests.get(details_url)
    if response.status_code == 200:
        details = response.json()
        image_url = details.get("primaryImage")
        title = details.get("title", "Unknown").replace("/", "-")
        year = details.get("objectDate", "Unknown")
        if image_url:
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                formatted_artist_name = artist_name.replace(" ", "_").replace("/", "-")
                formatted_title = title.replace(" ", "_").replace("/", "-")
                file_name = f"{formatted_artist_name}-{formatted_title}-{year}.jpg"
                file_path = os.path.join('images', file_name)  # Combine folder and file name

                with open(file_path, 'wb') as file:  # Open the file to write the image
                    for chunk in image_response.iter_content(1024):
                        file.write(chunk)
                print(f"Image for object ID {object_id} saved as {file_path}")
            else:
                print(f"Failed to download image for object ID {object_id}")
        else:
            print(f"No image URL for object ID {object_id}")
    else:
        print(f"Details not found for object ID {object_id}")

# Ensure the 'images' directory exists
ensure_directory_exists('images')

# Gather object IDs for all artists
all_object_ids = []
for artist in artists:
    object_ids = search_artworks_by_artist(artist)
    if object_ids:
        all_object_ids.extend([(id, artist) for id in object_ids])
        print(f"Found {len(object_ids)} artworks by {artist}")
    else:
        print(f"No artworks found for {artist}")

# Shuffle the list of object IDs if not empty
if all_object_ids:
    random.shuffle(all_object_ids)

    # Download images for the shuffled object IDs
    for object_id, artist_name in all_object_ids:
        fetch_and_save_artwork_image(object_id, artist_name)
        time.sleep(5)  # Sleep for 5 seconds before fetching the next image
else:
    print("No artworks found for the provided artists.")
