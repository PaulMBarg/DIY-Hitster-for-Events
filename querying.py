import requests
import authentication as auth
from error_fowarding import include_status
from importing_config import import_config

def spotify_query(searchterm=str, 
                  returned_types: list=["artist", "track", "album"], #@todo Does not work with just one single element
                  market: str="DE",
                  limit: int=10):

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

