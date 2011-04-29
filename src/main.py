import glob
import logging
import os
import sys
import urllib2

from django.utils import simplejson as json
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp import util, template

import appengine_utilities.sessions

def load_config():
    result = {}
    for conf in glob.glob('config/*.json'):
        try:
            if conf.endswith('.sample.json'):
                continue
            logging.info(conf)
            subconfig = json.load(open(conf, 'r'))
            name = os.path.splitext(os.path.basename(conf))[0]
            result[name] = subconfig
        except Exception, e:
            logging.error('Could not load subconfig "%s": %s' % (conf, e))
    return result

class BasicRequestHandler(webapp.RequestHandler):
    def initialize(self, request, response):
        webapp.RequestHandler.initialize(self, request, response)
        self.session = appengine_utilities.sessions.Session(writer='datastore')
        self.config = load_config()
    
    def get_base_url(self):
        return '../'*self.request.path.count('/')    
    
    def render(self, template_path, values):
        base_values = {
            'base_url': self.get_base_url(),
            'session': self.session,
            'config': self.config
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
from handlers.account import AccountHandler                                       
from handlers.user import UserProfileHandler

def main():   
    debug = os.environ['SERVER_SOFTWARE'].startswith('Development/')
    handlers = [
        ('/', MainHandler),
        ('/register/?', UserRegistrationHandler),
        ('/register/thanks/?', SuccessfulRegistrationHandler),
        ('/login/?', LoginHandler),
        ('/logout/?', LogoutHandler),
        ('/account/?', AccountHandler),
        ('/user/(.*?)/?', UserProfileHandler)
    ]
    application = webapp.WSGIApplication(handlers, debug=debug)
    util.run_wsgi_app(application)    