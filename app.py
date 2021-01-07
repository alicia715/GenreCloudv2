import spotipy
import spotipy.util as util
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import os
import service
import random
import io
import base64
import json
from flask import Flask, render_template, redirect, session, request, url_for

app = Flask(__name__,static_url_path='/static')
app.secret_key = "put secret key here"

@app.route("/auth")
def auth():
    return redirect(service.AUTH_URL)

@app.route("/callback/")
def callback():
    auth_token = request.args['code']
    access_token = service.authorize(auth_token)
    sp = spotipy.Spotify(auth=access_token) # session token
    session['access_token'] = access_token
    return redirect(url_for('genrecloud'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/guest')
def guest():
    sounds_dict = json.load(open('genreToPlaylist.json', 'r+'))
    genre_dict = json.load(open('guestData.json', 'r+'))
    return render_template('genre_cloud.html', genre_dict=genre_dict,
        sounds_dict=sounds_dict, username="", guest='true')

@app.route("/genrecloud", methods=["GET"])
def genrecloud():
    access_token = session['access_token']
    sp = spotipy.Spotify(auth=access_token)
    top_medium_term_artists = sp.current_user_top_artists(time_range='medium_term', limit=50)
    genre_dict = service.genreToArtists(top_medium_term_artists)
    sounds_dict = json.load(open('genreToPlaylist.json', 'r+'))
    username=sp.me()['display_name']
    return render_template('genre_cloud.html', genre_dict=genre_dict,
        sounds_dict=sounds_dict, username=username + "'s", guest='false')


#if __name__ == '__main__':
#    app.run(debug=True, host='127.0.0.1', port=3333)#debug=False, host='127.0.0.1', port=3333)
