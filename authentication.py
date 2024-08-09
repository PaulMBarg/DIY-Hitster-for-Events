import secrets
from importing_config import import_config
import requests
import time
from error_fowarding import include_status


SECRETS = import_config("secrets.json")
CONFIG = import_config("config.json")

CLIENT_ID = SECRETS["authentication"]["CLIENT_ID"]
CLIENT_SECRET = SECRETS["authentication"]["CLIENT_SECRET"]
ACCESS_TOKEN = {"token": None,
                "valid_until": None}

def authenticate():
    global ACCESS_TOKEN
    global CONFIG
    global SECRETS
    global CLIENT_ID
    global CLIENT_SECRET

    unix_current_time = int(time.time()) 

    if ((ACCESS_TOKEN["token"] is None) or 
        (ACCESS_TOKEN["valid_until"] < unix_current_time - 120)):
        refresh_authentication()
        #@todo no error fowarding here
    return ACCESS_TOKEN["token"]
    

def refresh_authentication():
    global ACCESS_TOKEN
    global CONFIG
    global SECRETS
    global CLIENT_ID
    global CLIENT_SECRET

    token_url = CONFIG["longterm_settings"]["spotify_api"]["token"]
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(token_url, headers=headers, data=data)
    response = check_http_response(response, "AuthError", CONFIG)
    if response["status"] == CONFIG["longterm_settings"]["statuscodes"]["Success"]:
        update_access_token(response["return"])
        return response
    else:
        return response
    

def check_http_response(response, potential_error_type):
    statuscodes = CONFIG["longterm_settings"]["statuscodes"]
    if hasattr(response, "error"):
        output = f"Error {response['error']['status']}: {response['error']['message']}."
        return include_status(output, statuscodes[potential_error_type])
    else:
        return include_status(response.json(), statuscodes["Success"])


def update_access_token(new_token):
    global ACCESS_TOKEN

    ACCESS_TOKEN["token"] = new_token["access_token"]
    ACCESS_TOKEN["valid_until"] = int(time.time()) + new_token["expires_in"]


