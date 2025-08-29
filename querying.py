import requests
import authentication as auth
import custom_exception as ce
from error_fowarding import include_status
from importing_config import import_config

def spotify_query(searchterm=str, 
                  returned_types: list=["artist", "track", "album"], #@todo Does not work with just one single element
                  market: str="DE",
                  limit: int=7):

    config = import_config("config.json")
    statuscodes = config["longterm_settings"]["statuscodes"]
    api_url = config["longterm_settings"]["spotify_api"]["search"]

    params = {"q": searchterm, 
              "type": ','.join(returned_types),
              "market": market, 
              "limit": limit}
    headers = {"Authorization": f"Bearer {auth.authenticate()}"}
    response = requests.get(api_url, params=params, headers=headers)
    
    if hasattr(response, "error"):
        output = f"Error {response['error']['status']}: {response['error']['message']}."
        return include_status(output, statuscodes["QueringError"])
    else:
        return include_status(response.json(), statuscodes["Success"])

def format_response(response: dict):
    songs = []
    for index, song in enumerate(response["return"]["tracks"]["items"]):    #seach only in tracks, not albums or artists
        
        #songtitle        
        song_title = song["name"]

        #artists
        try:
            artists = [artist["name"] for artist in song["artists"]]
        except KeyError:
            artists = ["unknown"]       # no artist in response (should not happen)
        if len(artists) > 1:
            artists = ", ".join(artists[:-1]) + " und " + str(artists[-1])
        else: 
            artists = artists[0]
    
        #release dates
        try:
            release_date = song["album"]["release_date"]
            release_year = release_date[:4]
            if int(release_year) > 2500 or int(release_year) < 1900:        #This will break in the year 2500 :)
                raise ce.DateFormatError(f"release_date = {release_date}")
        except KeyError:
            release_year = "unknown"     # no release_data in response
        except ce.DateFormatError:
            release_year = "unknown"

        #album
        try:
            album = song["album"]["name"]
        except KeyError:
            album = "unknown"     # no release_data in response

        #albumcover as url
        try:
            album_cover = song["album"]["images"][0]["url"]
        except KeyError:
            album_cover = "https://image.atsw.de/atsw/production/2024-03/1200x1200px_o_logo_o_schrift.jpg?fm=jpg&w=180&h=180&dpr=2"
            response = requests.get(album_cover)
            if not str(response.status_code).startswith("2"):
                raise ce.DeprecationError("The generic album cover is not available anymore.")
        
        # uri to create download link
        uri = song["uri"]

        songs += [{
            "title": song_title,
            "artist": artists,
            "album": album,
            "release_year": release_year,
            "album_cover_url": album_cover,
            "uri": uri
        }]


    return songs