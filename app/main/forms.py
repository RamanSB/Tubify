#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:19:49 2019

@author: RamanSB
"""

from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchSongForm(FlaskForm):
    search = TextField('Search song', validators=[DataRequired(), Length(min=1)])


class CreatePlaylistForm(FlaskForm):
    playlist_name = TextField('Playlist Name', validators=[DataRequired(), Length(min=1)])
    submit = SubmitField('Create')