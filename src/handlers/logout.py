from main import BasicRequestHandler

class LogoutHandler(BasicRequestHandler):
    def get(self):
        self.session.delete()
        self.redirect('/')