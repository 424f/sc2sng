from google.appengine.ext.webapp import util, template

from hashlib import sha1
import random

from main import BasicRequestHandler
from models import User

class LoginHandler(BasicRequestHandler):
    def get(self):
        if self.session.get('user', None) is not None:
            self.redirect('/')
            return
            
        self.render('templates/login.html', {})
        
    def post(self):
        if self.session.get('user', None) is not None:
            self.redirect('/')
            return
            
        # Verify login information
        user = User.all().filter('name =', self.request.get('username')).get()
        form_errors = {}
        
        if user is None:
            form_errors['username'] = 'A user with this name doesn\'t exist.'
        elif not user.check_password(self.request.get('password')):
            form_errors['password'] = 'Password is incorrect.'
        
        # Render login page (same as GET request)
        if len(form_errors) > 0:
            self.render('templates/login.html', {
                'form': dict([(key, self.request.get(key)) for key in self.request.arguments()]),
                'form_errors': form_errors
            })
            return
        
        # We're logged in now
        self.session['user'] = user.name
        self.redirect('/')