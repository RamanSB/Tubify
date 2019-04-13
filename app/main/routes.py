#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:19:11 2019

@author: RamanSB
"""
from flask import render_template, url_for, flash
from flask_login import current_user, login_required
from app.main import bp



@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title="Home")