#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:19:11 2019

@author: RamanSB
"""
from flask import render_template, url_for, flash
from flask_login import current_user, login_required
from app.main import bp
from app.main.forms import SearchSongForm



@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchSongForm()
    
    if(form.validate_on_submit()):
        current_user.spotify_authorize_user()
        print('PLACEHOLDER')
    return render_template('index.html', title="Home", form=form)