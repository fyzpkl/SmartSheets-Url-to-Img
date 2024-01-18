#from Smartsheets import *
import shutil
import requests
import json
import os



API_TOKEN = appName = os.getenv("SMARTSHEET_API_KEY")

sheet_Id = 'your_sheet_id'

def get_link_put_image(sheetId):
    header_get={
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }
    url = f'https://api.smartsheet.com/2.0/sheets/{sheetId}'

    response = requests.get(url, headers=header_get)
    sheet = response.json()
    for row in sheet ['rows']:
        row_id = row['id']
        image_link = None
        columnId = None
        for cell in row['cells']:
            if 'hyperlink' in cell:
                columnId = cell['columnId']
                image_link = cell['hyperlink']['url']
                break
        if image_link:
            file_name = download_image(image_link)
            add_image_from_directory(sheetId, columnId, row_id, file_name)

def download_image(image_link):
    file_name = image_link.split('/')[-1]
    directory_path = f"your_path\\"

    image_path = os.path.join(directory_path, file_name)
    response = requests.get(image_link, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        # Open the file in binary write mode and save the image
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Image successfully downloaded and saved to {image_path}")
    else:
        print("Failed to download image:", response.text)
    return file_name

def add_image_from_directory(sheetId, columnId, rowId, image_name):
    header_post = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json',
        'Content-Disposition': 'attachment; filename=Test_Sheet',
        'Content-Length': '5463'
    }
    file_path = f"your_path{image_name}"
    url = f'https://api.smartsheet.com/2.0/sheets/{sheetId}/rows/{rowId}/columns/{columnId}/cellimages'

    # Read the image in binary mode
    with open(file_path, 'rb') as image_file:
        image_data = image_file.read()
    # Make the POST request to upload the image
    response = requests.post(url, headers=header_post, data=image_data)
    # Check the response
    if response.status_code == 200:
        print("Image uploaded successfully")
    else:
        print("Failed to upload image:", response.text)

