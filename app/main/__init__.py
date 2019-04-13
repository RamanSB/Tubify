#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:16:34 2019

@author: RamanSB
"""

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes