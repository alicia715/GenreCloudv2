import spotipy
import spotipy.util as util
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import os

import base64
import requests
import json
import itertools
# Workaround to support both python 2 & 3
try:
    import urllib.request, urllib.error
    import urllib.parse as urllibparse
except ImportError:
    import urllib as urllibparse

os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = "https://genrecloud.azurewebsites.net/callback"

scope = 'user-top-read'

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": os.environ["SPOTIPY_REDIRECT_URI"],
    "scope": scope,
    "client_id": os.environ["SPOTIPY_CLIENT_ID"]
}

#python 3, making the url
if sys.version_info[0] >= 3:
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in list(auth_query_parameters.items())])
else:
    URL_ARGS = "&".join(["{}={}".format(key, urllibparse.quote(val))
                    for key, val in auth_query_parameters.iteritems()])

AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)

def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": os.environ["SPOTIPY_REDIRECT_URI"]
    }
    #python 3 or above
    if sys.version_info[0] >= 3:
        base64encoded = base64.b64encode(("{}:{}".format(os.environ["SPOTIPY_CLIENT_ID"], os.environ["SPOTIPY_CLIENT_SECRET"])).encode())
        headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    else:
        base64encoded = base64.b64encode("{}:{}".format(os.environ["SPOTIPY_CLIENT_ID"], os.environ["SPOTIPY_CLIENT_SECRET"]))
        headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)

    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    #return response_data
    access_token = response_data["access_token"]
    return access_token

# Creating a dictionary object that maps genre to artists
def genreToArtists(top_medium_term_artists):
    c_dict = {}
    for r in top_medium_term_artists['items']: # loop through each artist block
        for g in r['genres']: # loop through the genre of the artist
            if g in c_dict: # append to a dictionary, genre as the key and string of artists
                c_dict[g].append(r['name'])
            else:
                c_dict[g] = [r['name']]
    return c_dict
