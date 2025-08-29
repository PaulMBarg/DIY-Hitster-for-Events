import requests
import shutil
from creating_download_link import create_download_link
from datetime import datetime


def _check_string_in_file(file_path, string_to_check):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the entire content of the file
        file_content = file.read()
        # Check if the string is in the file content
        if string_to_check in file_content:
            return True
        else:
            return False

def _add_string_to_file(file_path, string_to_add):
    # Check if the string is already in the file
    if not _check_string_in_file(file_path, string_to_add):
        # Open the file in append mode to add the string
        current_time = datetime.now()
        with open(file_path, 'a') as file:
            file.write(string_to_add + '\n')


def download_code_img(uri, title, config):
    download_link = create_download_link(uri, **config["spotify_code"])
    spotify_code_image = requests.get(download_link, stream=True)

    # saving file 
    path_to_image = f"Downloads/{title}.{config['spotify_code']['image_format']}"
    with open(path_to_image, 'wb') as out_file:
        shutil.copyfileobj(spotify_code_image.raw, out_file)
    del spotify_code_image

    return path_to_image