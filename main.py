from flask import Flask, flash, redirect, render_template, request, session, abort
 
import sys
import spotipy
import spotipy.util as util

import random

from moodtape_functions import authenticate_spotify, aggregate_top_artists, aggregate_top_tracks, select_tracks, create_playlist

client_id = "blank"
client_secret = "blank"
redirect_uri = "blank"

scope = 'user-library-read user-top-read playlist-modify-public user-follow-read'

username = "mohithms"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)




app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('input.html')


@app.route("/", methods=['POST'])
def moodtape():
	mood = request.form['text']
	# username = request.form['username']
	mood = float(mood)
	# token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
	spotify_auth = authenticate_spotify(token)
	top_artists = aggregate_top_artists(spotify_auth)
	top_tracks = aggregate_top_tracks(spotify_auth, top_artists)
	selected_tracks = select_tracks(spotify_auth, top_tracks, mood)
	playlist = create_playlist(spotify_auth, selected_tracks, mood)
	return render_template('playlist.html', playlist=playlist )


if __name__ == "__main__":

	app.run(host='0.0.0.0')
