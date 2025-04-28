import os
import requests
import json
import shutil
from jinja2 import Environment, FileSystemLoader

# Define the path for the API key and read it
API_FILE_PATH = "/home/jortiz/secret_key.txt"
with open(API_FILE_PATH, "r") as file:
    api_key = file.read().strip()

API_URL = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&count=3"

# Folder paths
DOWNLOAD_DIR = "downloads"
BUILD_DIR = "build"
IMG_DIR = os.path.join(BUILD_DIR, "img")

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(IMG_DIR, exist_ok=True)

# Step 1: Make the API request
response = requests.get(API_URL)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Step 2: Download images
    image_paths = []
    for idx, item in enumerate(data):
        img_url = item.get("url")
        if img_url:
            # Download the image
            img_name = f"image_{idx + 1}.jpg"
            img_path = os.path.join(DOWNLOAD_DIR, img_name)
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)

            image_paths.append(img_path)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

# Step 3: Prepare image data for template rendering
images = [
    {
        'url': os.path.join('img', f"image_{idx + 1}.jpg"),  # Path to the image in the 'img' folder inside build
        'title': item['title'],
        'explanation': item['explanation']
    }
    for idx, item in enumerate(data)
]

# Step 4: Generate HTML with Jinja2
env = Environment(loader=FileSystemLoader('/home/jortiz/proj02/templates'))
template = env.get_template('newsletter-temp.html')

# Rendering HTML with the image data
context = {
    'title': 'Astronomy Picture of the Day',
    'images': images,  # Passing the image data to the template
}
html_content = template.render(context)

# Save the HTML to the build directory
html_output_path = os.path.join(BUILD_DIR, 'newsletter.html')
with open(html_output_path, 'w') as html_file:
    html_file.write(html_content)

print("Images downloaded and HTML generated successfully.")