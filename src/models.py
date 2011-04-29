from hashlib import sha1
import re

from google.appengine.ext import webapp, db
from django.core.validators import email_re
        
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
    salt = db.StringProperty(required=True)
    
    def check_password(self, password):
        return User.encode_password(password, self.salt) == self.password
    
    @staticmethod
    def encode_password(password, salt):
        return sha1(password + salt).hexdigest()
    
    @staticmethod
    def can_register(username, email):
        result = {}
        
        # Make sure username is valid and not in use
        if not re.match('[0-9_-a-zA-Z]', username):
            result['username'] = 'Username must only contain alphanumeric characters and the special characters -, _.'
        elif User.all().filter('name =', username).count(limit=1) > 0:
            result['username'] = 'The username %s is already in use.' % username
            
        # Email has to be valid and unique
        if not email_re.match(email):
            result['email'] = 'Please enter a valid e-mail address.'
        elif User.all().filter('email =', email).count(limit=1) > 0:
            result['email'] = 'The e-mail address %s is already in use.' % email

        return (len(result) == 0, result)
            

class TournamentRegistration(db.Model):
    user_key = db.StringProperty(required=True)
    start_time = db.DateTimeProperty(required=True)
    end_time = db.DateTimeProperty(required=True)