from google.appengine.ext.webapp import util, template

from hashlib import sha1
import random

from main import BasicRequestHandler
from models import User

class UserRegistrationHandler(BasicRequestHandler):
    def get(self):
        if self.session.get('user', None) is not None:
            self.redirect('/')
            return
            
        self.render('templates/register.html', {})
        
    def post(self):
        if self.session.get('user', None) is not None:
            raise Exception("Cannot register user when already logged in.")

        # Make sure the user can be registered
        can_register, form_errors = User.can_register(username=self.request.get('username'), email=self.request.get('email'))
        
        # Repeated password should also match
        min_password_length = 6
        password, password_repeat = self.request.get('password'), self.request.get('password_repeat')
        if password != password_repeat:
            can_register = False
            form_errors['password_repeat'] = 'Entered passwords don\'t match.'
        if len(password) < min_password_length:
            can_register = False
            form_errors['password'] = 'Please enter a password with at least %d characters.' % min_password_length
        
        # Render registration page (same as GET request)
        if not can_register:
            self.render('templates/register.html', {
                'form': dict([(key, self.request.get(key)) for key in self.request.arguments()]),
                'form_errors': form_errors
            })
            return
        
        # Let's register!
        name = self.request.get('username')
        salt = sha1(str(random.random())).hexdigest()
        password = self.request.get('password')
        email = self.request.get('email')
        
        user = User(name=name, salt=salt, password=User.encode_password(password, salt), email=email)
        user.put()
        
        self.session['user'] = name
            
        self.redirect('/register/thanks')
            
class SuccessfulRegistrationHandler(BasicRequestHandler):
    def get(self):
        self.render('templates/register-thanks.html', {})