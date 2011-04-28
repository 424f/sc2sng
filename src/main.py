import logging
import os
import sys
import urllib2

from django.utils import simplejson as json
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template

import appengine_utilities.sessions

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

class BasicRequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.session = appengine_utilities.sessions.Session(writer='datastore')
    
class MainHandler(BasicRequestHandler):
    def get(self):
        self.session['visited'] = self.session.get('visited', 0) + 1
        self.response.out.write(self.session['visited'])
        #self.response.out.write(template.render('templates/index.html', {}))

from handlers.user_registration import UserRegistrationHandler        

def main():   
    debug = os.environ['SERVER_SOFTWARE'].startswith('Development/')
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=debug)
    util.run_wsgi_app(application)    