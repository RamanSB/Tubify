#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:20:00 2019

@author: RamanSB
"""

from app import db
from app.auth import bp
from flask_login import current_user, login_user, logout_user
from app.auth.forms import LoginForm, RegistrationForm
from flask import request, url_for, redirect, render_template, flash, current_app
from werkzeug.urls import url_parse
from app.models import User
import requests
import json


'''
ToDo: - Create main blueprint routes.
      - Create Login & Register templates.
'''

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if(current_user.is_authenticated):
        return redirect(url_for('main.index'))
    form = LoginForm()
    if(form.validate_on_submit()):
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Please try again.")
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if(not next_page or url_parse(next_page).netloc != ''):
            next_page = (url_for('main.index'))
        return redirect(next_page)
    return render_template('login.html', form=form)

@bp.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if(current_user.is_authenticated):
        return redirect(url_for('main.index')) 
    form = RegistrationForm()
    if(form.validate_on_submit()):
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user.")
        return redirect(url_for('auth.login')) #This will call the auth blueprints login endpoint which will render the login template on a GET request.
    return render_template('register.html', title="Register", form=form)

@bp.route('/authorize/spotify/<string:user>', methods=['GET', 'POST'])
def authorize_spotify_user(user):
    if(current_user.is_authenticated):
        print('Authorize spotify')
        response =  current_user.spotify_authorize_user()
        #authorization_header = {"Authorization": "Bearer {}".format(access_token)}
        return redirect(response.url)
    
            
        