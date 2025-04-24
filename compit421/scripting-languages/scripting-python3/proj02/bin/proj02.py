import os
import requests
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Define the path for the API key
API_FILE_PATH = "/home/jortiz/secret_key.txt"
API_URL = "https://api.nasa.gov/planetary/apod"

# Folder paths
DOWNLOAD_DIR = "downloads"
BUILD_DIR = "build"
IMG_DIR = os.path.join(BUILD_DIR, "img")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Function to extract three random APOD entries of the data
def fetch_apod_data(api_key, count=3):
    """Fetch random APOD entries from NASA API."""
    apod_entries = []
    index = 1
    while len(apod_entries) < count:
        random_date = get_random_apod_date()
        params = {
            "api_key": api_key,
            "date": random_date
        }
        response = requests.get(NASA_APOD_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            # We only want entries with images, not videos
            if data.get("media_type") == "image":
                # Extract only the needed information
                image_url = data.get("url", "")
                date_str = data.get("date", "")
                # Download with custom filename
                image_name = download_image(image_url, index, date_str)
                if image_name:
                    apod_entry = {
                        "copyright": data.get("copyright", "NASA"),
                        "date": date_str,
                        "image_name": image_name,
                        "title": data.get("title", ""),
                        "explanation": data.get("explanation", "")
                    }
                    apod_entries.append(apod_entry)
                    index += 1
    return apod_entries
# Function to download images
def download_image(url, index, entry_date):
    """Download an image to the downloads directory with custom naming."""
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)
    # Create a filename based on date and index
    filename = f"apod_{entry_date}_{index}.jpg"
    file_path = os.path.join(DOWNLOADS_DIR, filename)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
        print(f"Image saved to {file_path}")
        return filename
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

# Function to jinjafy the newsletter
def generate_newsletter(apod_entries):
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("newsletter.html.j2")
    # Render the newsletter
    rendered_newsletter = template.render(entries=apod_entries)
    # Save the newsletter HTML file
    os.makedirs(BUILD_DIR, exist_ok=True)
    newsletter_path = os.path.join(BUILD_DIR, "newsletter.html")
    with open(newsletter_path, "w") as f:
        f.write(rendered_newsletter)
    print(f"Newsletter generated: {newsletter_path}")

# Function to copy images to the build/img directory
def move_images_to_build(apod_entries):
    for entry in apod_entries:
        image_filename = entry["image_filename"]
        image_path = os.path.join(DOWNLOAD_DIR, image_filename)
        destination = os.path.join(IMG_DIR, image_filename)

        if os.path.exists(image_path):
            shutil.copy(image_path, destination)
            print(f"Copied image {image_filename} to {IMG_DIR}")
        else:
            print(f"Image {image_filename} not found in {DOWNLOAD_DIR}")

# Main workflow
def main():
    # Extract the APOD entries
    apod_entries = extract_apod_data(num_entries=3)
    # Download the images
    download_images(apod_entries)
    # Generate the newsletter using Jinja
    generate_newsletter(apod_entries)
    # Move the images to build/img
    move_images_to_build(apod_entries)

if __name__ == "__main__":
    main()
