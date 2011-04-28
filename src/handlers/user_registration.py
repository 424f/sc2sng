from main import BasicRequestHandler

class UserRegistrationHandler(BasicRequestHandler):
    def get():
        if self.session.get('user', None) is not None:
            raise Exception("Cannot register user when already logged in.")
        self.response.out.write(template.render('templates/registration.html', {}))
        
    def post():
        if self.session.get('user', None) is not None:
            raise Exception("Cannot register user when already logged in.")