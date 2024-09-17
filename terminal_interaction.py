import json
import requests
import shutil
import authentication as auth
from OneClick_font import oneclick
from querying import spotify_query
from creating_download_link import create_download_link
from importing_config import import_config

running = True

print(oneclick)     # welcome message

config = import_config("config.json")

while running:
    query = input("Welchen Song willst du suchen? ")

    response = spotify_query(searchterm=query)

    print("\nIch habe folgende Songs gefunden: \n")
    for index, song in enumerate(response["return"]["tracks"]["items"]):
        song_title = song["name"]
        artists = [artist["name"] for artist in song["artists"]]
        if len(artists) > 1:
            artists = ", ".join(artists[:-1]) + " und " + str(artists[-1])
        else: 
            artists = artists[0]
        print(f"{index+1}: {song_title}, {artists}")
    
    index_answer = input("Welchen der Songs meinst du? Schreibe einfach die Nummer vor dem Song: ")

    try: 
        if int(index_answer) not in range(1, index+2):
            print("Deine Eingabe ist nicht innerhalb des richtigen Zahlenbereichs.")
            continue
    except ValueError:
        print("Du musst eine Zahl eingeben.")
        continue
    # check if index is valid

    song_uri = response["return"]["tracks"]["items"][int(index_answer)-1]["uri"]
    song_name = response["return"]["tracks"]["items"][int(index_answer)-1]["name"]
    download_link = create_download_link(song_uri, **config["spotify_code"])

    spotify_code_image = requests.get(download_link, stream=True)

    # saving file 
    with open(f"Downloads/{song_name}.{config['spotify_code']['image_format']}", 'wb') as out_file:
        shutil.copyfileobj(spotify_code_image.raw, out_file)
    del spotify_code_image

    print("Erfolgreich gesichert.\n \n")
