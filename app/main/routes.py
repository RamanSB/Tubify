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
from app.main.forms import SearchSongForm
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
        #return(redirect(url_for('main.index')))
    
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


@bp.route('/add_to_playlist', methods=['GET'])
def add_to_playlist():
    print()