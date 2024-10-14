import querying
import custom_exception as ce
from flask import Flask, render_template, request, jsonify

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

    # TODO proper error handling!!!!
    songs = [{
        "title": e,
        "artist": 1,
        "album": 2
        }]
    return jsonify(songs)
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
