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
    songs = [
        {"title": "Song Title 1", "artist": "Artist Name 1", "album": "Album Name 1", "album_cover_url": "https://99designs-blog.imgix.net/blog/wp-content/uploads/2019/07/attachment_105309522-e1565728357170.jpg?auto=format&q=60&fit=max&w=930"},
        {"title": "Song Title 2", "artist": "Artist Name 2", "album": "Album Name 2"},
        {"title": "Song Title 3", "artist": "Artist Name 3", "album": "Album Name 3"},
        {"title": "Song Title 1", "artist": "Artist Name 1", "album": "Album Name 1"},
        {"title": "Song Title 2", "artist": "Artist Name 2", "album": "Album Name 2"},
        {"title": "Song Title 3", "artist": "Artist Name 3", "album": "Album Name 3"},
        {"title": "Song Title 1", "artist": "Artist Name 1", "album": "Album Name 1"},
        {"title": "Song Title 2", "artist": "Artist Name 2", "album": "Album Name 2"},
        {"title": "Song Title 3", "artist": "Artist Name 3", "album": "Album Name 3"}
    ]

    return jsonify(songs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
