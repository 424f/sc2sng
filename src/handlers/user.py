from google.appengine.ext.webapp import template

from main import BasicRequestHandler
from models import User

class UserProfileHandler(BasicRequestHandler):
    def get(self, username):
        user = User.all().filter('name =', username).get()
        if user is None:
            self.render('templates/user.html', {'error': 'User %s does not exist.' % username})
            return
            
        self.render('templates/user.html', {'user': user})