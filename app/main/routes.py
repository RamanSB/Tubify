#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:19:11 2019

@author: RamanSB
"""
from flask import render_template, url_for, flash, request, current_app, redirect
from flask_login import current_user, login_required
from app.main import bp
from app import db
from app.main.forms import SearchSongForm, CreatePlaylistForm
from app.models import Playlist
from werkzeug.urls import url_parse
import json
import requests



@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    print('main.index')
    form = SearchSongForm()
   
    if(form.validate_on_submit()):
        search = form.search.data
        results = current_user.spotify_search_song(search)
        return render_template('index.html', title="Home", form=form, track_data=results)
    
    auth_token = request.args.get('code')
    print('Auth token:' + str(auth_token))
    if(auth_token is not None):
        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": "http://0.0.0.0:5000/index",
            'client_id': current_app.config['SPOTIFY_CLIENT_ID'],
            'client_secret': current_app.config['SPOTIFY_SECRET_KEY'],
        }
        post_response = requests.post(current_app.config['SPOTIFY_TOKEN_ENDPOINT'], data=code_payload)
    
        response_data = json.loads(post_response.text)
        print(post_response.text)
        access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']
        token_type = response_data['token_type']
        expires_in = response_data["expires_in"]
        current_user.set_spotify_access_token(access_token)
        db.session.commit()

    return render_template('index.html', title="Home", form=form)


@bp.route('/<user>/playlists', methods=['GET', 'POST'])
@login_required
def playlists(user):
    form = CreatePlaylistForm()
    print('playlist endpoint')
    if(form.validate_on_submit()):
        print('[Playlists] form.validate_on_submit')
        playlist_name = request.form.get('playlist_name', None)
        return redirect(url_for('main.create_playlist', user=current_user.username, playlist_name=playlist_name))
    return render_template('playlists.html', form=form)


@bp.route('/<string:user>/playlists/create/<string:playlist_name>', methods=['GET'])
@login_required
def create_playlist(user, playlist_name):
    print('[Create_Playlist] :' + str(playlist_name))
    current_user.create_playlist(playlist_name)
    db.session.commit()
    flash("Playlist has been successfully created")
    return redirect(url_for('main.playlists', user=current_user.username))


@bp.route('/<string:user>/playlists/<string:playlist_name>/add/<song_name>_<string:song_length>_<song_url>', methods=['GET'])
@bp.route('/<string:user>/playlists/<string:playlist_name>/add/<song_name>_<song_url>', methods=['GET'])
@login_required
def add_song_to_playlist(user, playlist_name, song_name, song_length, song_url):
    print('[Add_Song_To_Playlist] | ' + song_name + '|||' + song_url + '|||' + song_length)
    #song_name = song_data['track_name']
    #s = Song()
    #print('[Add_Song_To_Playlist] | ' + str(playlist_name) + str(song_name))
    playlist = Playlist.query.filter_by(title=playlist_name).first()
    if(playlist is None):
        print('PLACEHOLDER | playlist does not exist')
    
    return redirect(url_for('main.index'))
    
 
    