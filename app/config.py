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
    
    

    
    