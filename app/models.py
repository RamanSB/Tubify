#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:51:43 2019

@author: RamanSB

Define Models [Schema]: 
    - User [user_id, username, email, password_hash]
    - Song [song_id, title, length, artist_id]
    - Playlist [playlist_id, title, user_id]
    - Artist [artist_id, name]
    
Relationships:
    1) A User may have many playlist(s) (One-Many) - backref: creator, playlist.cr
    -eator shall return the user creating the playlist.
    
    2) No relation between User and Song? The relationship between user and son
    -gs is through Playlist and song(s).
    
    3) A playlist may contain many song(s) and a song can be apart of many play
    -list(s) (Many-Many)
    
    4) User - Artists (No relation) 
    
    5) Playlist-Artist, a particular Artist may appear on many playlist(s) and
    a playlist can contain multiple Artist(s) [Many-Many]
    
    6) Artist - Song, Multiple artist(s) can appear on one song. Multiple song(s)
    can be created by an Artist. [Many-Many]
    
    Will require  3 Association Tables (playlists_artists, playlists_songs, artists_songs)
"""

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask import current_app
import requests
import math

#Association table for MANY-MANY relationship between Playlist(s) and Song(s)
playlists_songs = db.Table('playlists_songs',
        db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
        db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
    )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    playlists = db.relationship('Playlist', backref='creator', lazy='dynamic')
    spotify_token = db.relationship('SpotifyToken', backref="token_owner", uselist=False, lazy=True)
    
    
    def __repr__(self):
        return f"<User: {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    #https://accounts.spotify.com/authorize?client_id=5fe01282e44241328a84e7c5cc169165
    #&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&scope=user-read-private%20user-read-email&state=34fFs29kd09
    def spotify_authorize_user(self):
        print("Spotify - Authorize End Point")
        myparams = {'client_id':current_app.config['SPOTIFY_CLIENT_ID'],
                    'response_type':'code',
                    'redirect_uri':'http://0.0.0.0:5000/index'}
        response = requests.get(current_app.config['SPOTIFY_AUTHORIZE_ENDPOINT'], params=myparams)
        print(response.url)
        return response
    

    #https://api.spotify.com/v1/search?q=name:abacab&type=album,track (query string)
    def spotify_search_song(self, song_name):
        print("Spotify - Search Song End Point")
        myparams = {'type':'track'}
        myparams['q']=song_name
        authorization_header = {"Authorization": "Bearer {}".format(current_user.spotify_token.token)}
        print("AuthHeader\n"+str(authorization_header))
        response = requests.get(current_app.config['SPOTIFY_SEARCH_ENDPOINT'], params=myparams, headers=authorization_header)
        response_body = response.json()['tracks']['items']
        results_data = []
        for i in range(len(response_body)):
            track_name = response_body[i]['name']
            artist_name = response_body[i]['album']['artists'][0]['name']
            album_name = response_body[i]['album']['name']
            track_length = convert_ms_to_length(int(response_body[i]['duration_ms']))
            href = response_body[i]['href']
            preview_url = response_body[i]['preview_url']
            uri = response_body[i]['uri']

            item_data = {'track_name':track_name,
                         'album_name':album_name,
                         'artist_name':artist_name,
                         'length':track_length,
                         'preview_url':preview_url,
                         'uri':uri,
                         'href':href
                         }
            results_data.append(item_data)
      
        print(len(results_data))
        return results_data
        
    def set_spotify_access_token(self, access_token):
        st = SpotifyToken(token=access_token, token_owner=self)
        db.session.add(st)
     
        
    
    
#Load user function (Required for: )
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    artist_id = db.Column(db.Integer, index=True)
    #length = db.Column(db.) Not sure do I use datetime or just String.

    def __repr__(self):
        return f"<Song: {self.title}>"
    
    
class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f"<Artist: {self.name}>"
    
    
class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    songs = db.relationship('Song', secondary=playlists_songs, 
                            lazy='subquery', 
                            backref=db.backref('host_playlist',lazy=True))

    def __repr__(self):
        return f"<Playlist: {self.title}>"


class SpotifyToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    token = db.Column(db.Text)



def convert_ms_to_length(duration_ms):
    minutes = duration_ms * 0.00001666667
    if(minutes>1):
        noOfMins = int(minutes)
        minFracs = minutes - noOfMins
        noOfSecs = math.floor(minFracs * 60)
        if(noOfSecs<10):
            str(noOfMins)+":0"+str(noOfSecs)
        elif(noOfSecs>60):
           return 'x:xx'
        else:
            return str(noOfMins)+":"+str(noOfSecs)
    else:
        return "0:"+str(round(minutes*60))
        