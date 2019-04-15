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
from flask_login import UserMixin
from flask import current_app
import requests

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
                    'redirect_uri':'0.0.0.0:5000/index'}
        request = requests.get(current_app.config['SPOTIFY_AUTHORIZE_ENDPOINT'], params=myparams)
        print(request.json())
    
    #https://api.spotify.com/v1/search?q=name:abacab&type=album,track (query string)
    def spotify_search_song(self, song_name):
        print("Spotify - Search Song End Point")
        myparams = {'type':'track'}
        myparams['q']=song_name
        request = requests.get(current_app.config['SPOTIFY_SEARCH_ENDPOINT'], params=myparams)
        
        
    
    
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
