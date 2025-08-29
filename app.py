import querying
import requests
import shutil
import custom_exception as ce
import utils as u
import traceback
import catprinter_main.catprint_cmd as cp 
from flask import Flask, render_template, request, jsonify
from creating_download_link import create_download_link
from importing_config import import_config


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_input = data.get('user_input')
    
    # Beispiel-Daten für den Response

    try:
        respone = querying.spotify_query(searchterm=user_input)
    except:
        print("ERROR with query")      # implemt proper error handling

    try:
        songs = querying.format_response(respone)
        return jsonify(songs)
    except NameError:
        e = "ERROR with query"
    except ce.DeprecationError as DE:
        e = "ERROR with image"
    except:
        e = "unkown error with formatting"

    # @todo TODO proper error handling!!!!

    if len(user_input) == 0:
        songs = [{
            "title": "Gebe etwas in die SUCHLEISTE ein.",
            "artist": " ",
            "album": " "
            }]
    else:
        songs = [{
            "title": "KEINE INTERNETVERBINDUNG",
            "artist": " ",
            "album": " "
            }]
    return jsonify(songs)

@app.route('/catprint', methods=['POST'])
def catprint():

    print("Start with request")

    data = request.json
    uri = data.get('uri')
    title = data.get("title")
    year = data.get("release_year")
    album = data.get("album")
    artist = data.get("artist")
    album_cover_url = data.get("album_cover_url")

    print("uri: ", uri)
    print("title: ", title)


    try:
        if u._check_string_in_file("Downloads/list.txt", title + artist):    # title already downloaded
            raise ce.SongChosenTwice("Someone else chosed this song.")
    except ce.SongChosenTwice as e: 
        print("SongChosenTwice: ", str(e))
        response = {
            "status_code": 403,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
        return jsonify(response)


    config = import_config("config.json")
    
    try:
        path_to_code = u.download_code_img(uri, title, config)
    except Exception as e:
        print("Error with Download: ", str(e))
        response = {
            "status_code": 408,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
        return jsonify(response)


    print_kargs = {         # args that are needed by catprinter repo, default from cp.parse_args()
        "filename": path_to_code,
        "log_level": "info",
        "img_binarization_algo": 'mean-threshold',
        "show_preview": False,
        "device": '',
        "energy": int("0xffff".removeprefix("0x"), 16)
    }

    try:
        cp.print_with_catprinter(print_kargs)
    except FileNotFoundError as e:
        print("FileNotFoundError: ", str(e))
        response = {
            "status_code": 400,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
    except RuntimeError as e:
        print("RuntimeError: ", str(e))
        response = {
            "status_code": 407,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
    except ce.PrinterNotFound as e:
        print("PrinterNotFound: ", str(e))
        response = {
            "status_code": 404,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
    except ce.OutOfPaper as e:
        print("OutOfPaper: ", str(e))
        response = {
            "status_code": 401,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
    except Exception as e:
        print("Unkown: ", type(e), " ", str(e))
        response = {
            "status_code": 402,
            "error_type": str(type(e)),
            "error_msg": str(e)
        }
    else:
        response = {
            "status_code": 200,
            "title": title,
            "album_cover_url": album_cover_url,
            "artist": artist,
            "album": album,
            "release_year": year
        }
        u._add_string_to_file("Downloads/list.txt", title + artist)


    print("READY")
    print(response, type(response),)
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
