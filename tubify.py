#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:33:05 2019

@author: RamanSB

ToDo: import models from app.models, then add the model entities to a shell
context (using @app.shell_context_processor decorater)
"""

from app import create_app, db
from app.models import User, Artist, Playlist, Song, SpotifyToken

app = create_app()

@app.shell_context_processor
def make_context():
    return {'db': db, 'User': User, 'Playlist': Playlist, 'Song': Song,
            'Artist': Artist}
