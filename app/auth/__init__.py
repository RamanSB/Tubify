#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:03:55 2019

@author: RamanSB

Creating auth blueprint which will be registered with Flask app within
app package initializer. We also import the endpoints this auth blueprint 
modules uses.
"""

from flask import Blueprint

bp = Blueprint('auth',__name__)

from app.auth import routes
