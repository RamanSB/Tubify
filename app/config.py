#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 13:52:10 2019

@author: RamanSB
"""

'''
ToDo: 
- Will Also include endpoint request urls from Spotify WEB API + Youtube WEB API
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'never-gonna-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #Spotify API End-points
    SPOTIFY_SECRET_KEY = "a80afe19c09e4c68877ba539e9f5b1b8"
    SPOTIFY_CLIENT_ID = "5672cca96bb442979a52f9e5d9f2c71e"
    SPOTIFY_AUTHORIZE_ENDPOINT = "https://accounts.spotify.com/authorize"
    SPOTIFY_SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
    SPOTIFY_TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
    
    
    

    
    