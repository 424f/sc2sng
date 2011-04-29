from google.appengine.ext.webapp import util, template

from hashlib import sha1
import random

from main import BasicRequestHandler
from models import User

def authenticate(f):
    def _f(self, *args, **kwargs):
        if self.session.get('user', None) is None:
            raise Exception("You need to be authenticated to do that.")
        return f(self, *args, **kwargs)
    return _f

class AccountHandler(BasicRequestHandler):
    @authenticate
    def get(self):            
        self.render('templates/account.html', {})
    
    @authenticate
    def post(self):
        pass