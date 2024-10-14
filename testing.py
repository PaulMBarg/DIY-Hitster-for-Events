import querying
from flask import Flask, render_template, request, jsonify
import custom_exception as ce

user_input = "Miachel"

def process(user_input):
    try:
        respone = querying.spotify_query(searchterm=user_input)
    except:
        e = "ERROR with query"      # implemt proper error handling

    try:
        songs = querying.format_response(respone)
        return songs
    except NameError:
        e = "ERROR with query"
    except ce.DeprecationError as DE:
        e = "ERROR with image"
    except:
        e = "unkown error with formatting"


    songs = [{
        "title": e,
        "artist": 1,
        "album": 2
        }]

songs = process(user_input)

print(songs)