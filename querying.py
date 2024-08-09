import requests
import output
from error_fowarding import include_status
from importing_config import import_config

def spotify_query(searchterm=str, 
                  returned_types: list=["artists, playlist, albums"], #@todo Does not work with just one single element
                  market: str="DE",
                  limit: int=10):

    config = import_config("config.json")
    statuscodes = config["longterm_settings"]["statuscodes"]
    api_url = config["longterm_settings"]["spotify_api"]["search"]

    params = {"q": searchterm, 
              "type": ','.join(returned_types),
              "market": market, 
              "limit": limit}
    response = requests.get(api_url, params=params)
    
    if hasattr(response, "error"):
        output = f"Error {response['error']['status']}: {response['error']['message']}."
        return include_status(output, statuscodes["QueringError"])
    else:
        return include_status(response.json(), statuscodes["Success"])

#if spotify query raises an unexpected error, it is not gonna be fowarded
response = spotify_query("Alligatoah")
output.echo("print", response)

