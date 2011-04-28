#!/usr/bin/env python

import logging
import os
import sys
import urllib2

from django.utils import simplejson as json
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template

sys.path += [os.path.join(os.path.dirname(__file__), 'src')]

class Tournament(db.Model):
    id = db.IntegerProperty(required=True)
    players = db.ListProperty(int, required=True)
    has_started = db.BooleanProperty(required=True)

class Account(db.Model):
    user_key = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    code = db.IntegerProperty(required=True)
    realm = db.StringProperty(required=True)
    
class User(db.Model):
    name = db.StringProperty(required=True)
    email = db.EmailProperty(required=True)
    password = db.StringProperty(required=True)
    password_salt = db.StringProperty(required=True)

class TournamentRegistration(db.Model):
    user_key = db.StringProperty(required=True)
    start_time = db.DateTimeProperty(required=True)
    end_time = db.DateTimeProperty(required=True)
    
class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Hey there.')
   

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)    

if __name__ == '__main__':
    main()
