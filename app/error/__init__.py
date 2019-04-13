#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:18:00 2019

@author: RamanSB
"""

from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers