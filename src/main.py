import logging
import os
import sys
import urllib2

from django.utils import simplejson as json
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template

import appengine_utilities.sessions

class BasicRequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.session = appengine_utilities.sessions.Session(writer='datastore')
    
    def get_base_url(self):
        return '../'*self.request.path.count('/')    
    
    def render(self, template_path, values):
        base_values = {
            'base_url': self.get_base_url(),
            'session': self.session
        }
        base_values.update(values)
        self.response.out.write(template.render(template_path, base_values))
    
class MainHandler(BasicRequestHandler):
    def get(self):
        self.render('templates/index.html', {})

from handlers.login import LoginHandler                                       
from handlers.logout import LogoutHandler        
from handlers.user_registration import UserRegistrationHandler, \
                                       SuccessfulRegistrationHandler       

def main():   
    debug = os.environ['SERVER_SOFTWARE'].startswith('Development/')
    handlers = [
        ('/', MainHandler),
        ('/register/?', UserRegistrationHandler),
        ('/register/thanks/?', SuccessfulRegistrationHandler),
        ('/login/?', LoginHandler),
        ('/logout/?', LogoutHandler)
    ]
    application = webapp.WSGIApplication(handlers, debug=debug)
    util.run_wsgi_app(application)    