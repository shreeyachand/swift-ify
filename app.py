from os import environ
from flask import Flask, session, request, redirect, url_for, render_template
from flask_session import Session
from requests import auth
import spotipy, uuid, os, pickle
import numpy as np
import pandas as pd
from subs import fetch_tv_id

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path():
    return caches_folder + session.get('uuid')

def get_auth():
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path())
    return cache_handler, spotipy.oauth2.SpotifyOAuth(client_id=environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=environ.get("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=url_for("redirect_page", _external=True), scope='playlist-modify-public user-library-read', cache_handler=cache_handler, show_dialog=True)

@app.route('/')
def index():
    return redirect(url_for('redirect_page'))

@app.route('/redirect')
def redirect_page():
    if not session.get('uuid'):
        # Step 1. Visitor is unknown, give random ID
        session['uuid'] = str(uuid.uuid4())

    cache_handler, auth_manager = get_auth()

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        auth_manager.get_access_token(request.args.get("code"))
        return redirect('/redirect')

    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        # Step 2. Display sign in link when no token
        auth_url = auth_manager.get_authorize_url()
        return render_template("home.html", auth_url=auth_url, out=True)

    # Step 4. Signed in, display data
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return redirect('/playlists')

@app.route('/logout')
def sign_out():
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        os.remove(session_cache_path())
        session.clear()
        return render_template("loggedout.html", out=True)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
        return "Unsuccessful"
    except TypeError as e:
        return redirect('/')


@app.route('/playlists', methods=["GET", "POST"])
def playlists():
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    results = sp.current_user_playlists()

    #if request.method == "POST":
    #    playlistid = request.form.get('comp_select')
    #   return render_template('playlist.html', playlist_data=results['items'], user_info=sp.current_user(), pfp=get_pfp(sp.current_user()), id=playlistid)
    if request.method == "POST":
        playlistids = request.form.get('listIds').split(',')[0]
        return tfy(playlistids)
    else:
        return render_template('dropdown.html', playlist_data=results['items'], user_info=sp.current_user(), pfp=get_pfp(sp.current_user()))

def tfy(args):
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    if args=="":
        return "you didn't select any playlists! try again."
    sp = spotipy.Spotify(auth_manager=auth_manager)
    chosenIds = args.split(',')
    for id in chosenIds:
        for x, song in enumerate(get_playlist_tracks(id)):
            if (fetch_tv_id(song['track']['id'])) != -1:
                sp.playlist_remove_specific_occurrences_of_items(id, [{"uri":song['track']['id'], "positions":[x]}])
                sp.playlist_add_items(id, [fetch_tv_id(song['track']['id'])], position=x)
    return redirect('/success')
        

@app.route('/success')
def success():
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return render_template('success.html', user_info=sp.current_user(), pfp=get_pfp(sp.current_user()))


def get_pfp(info):
    if len(info['images']) < 1:
        return 'https://t4.ftcdn.net/jpg/00/64/67/63/360_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg'
    else:
        return info['images'][0]['url']

# filters used to render playlist pic and title
@app.template_filter('image')
def get_playlist_img(id):
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    data = sp.playlist(id)
    return data['images'][0]['url']

@app.template_filter('title')
def get_playlist_title(id):
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')

    sp = spotipy.Spotify(auth_manager=auth_manager)
    data = sp.playlist(id)
    return data['name']

@app.template_filter('tracks')
def get_playlist_tracks(id):
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp.playlist_items(id)['items']

@app.route('/recommendations', methods=["GET", "POST"])
def recommendations():
    cache_handler, auth_manager = get_auth()
    if not auth_manager.validate_token(cache_handler.get_cached_token()):
        return redirect('/')
    sp = spotipy.Spotify(auth_manager=auth_manager)
    if request.method == "POST":
        id = request.form.get("playid")
        return render_template("reccs.html", user_info=sp.current_user(), pfp=get_pfp(sp.current_user()), id=id)

def get_song_name(id):
    cache_handler, auth_manager = get_auth()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
@app.template_filter('trackname')
def trackname(id):
    cache_handler, auth_manager = get_auth()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    track_info = sp.tracks(id)
    return list(track_info['tracks'])

@app.route('/add', methods=["GET", "POST"])
def add():
    cache_handler, auth_manager = get_auth()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    if request.method == "POST":
        play_id = request.form.get('playlistId')
        track_ids = request.form.get('trackIds').split(',')
        sp.playlist_add_items(play_id, track_ids)
        return render_template("added.html", user_info=sp.current_user(), pfp=get_pfp(sp.current_user()))
    else:
        return redirect('/playlists')

if __name__ == '__main__':
    app.run(threaded=True, port=int(os.environ.get("PORT",
                                    os.environ.get("SPOTIPY_REDIRECT_URI", 8080).split(":")[-1])))
