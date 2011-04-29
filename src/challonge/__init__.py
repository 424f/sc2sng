import urllib, urllib2
from xml.etree.ElementTree import XMLParser

class TournamentConstructor:
    tournaments = []
    t = None

    def start(self, tag, attrib):
        if tag == "tournament":
            self.t = {}
        elif self.t != None:
            print tag, attrib
            self.t['tag'] = None
    
    def end(self, tag):
        if tag == "tournament":
            self.t = None
            self.tournaments.append(self.t)
    
    def data(self, data):
        print data
    
    def close(self):
        return self.tournaments

class Challonge:
    
    CHALLONGE_BASE_URL = "https://challonge.com/api/"
    
    def __init__(self, api, response):
        self.api_key = api
        self.response_format = response
        
    def get_tournaments(self, **kwargs):
        """
        Returns set of tournaments from Challonge
        Keywords:
        state: One of { all, pending, in_progress, ended }
        type: One of { single_elimination, double_elimination, round_robin, swiss }
        created_after: YYYY-MM-DD
        created_before: YYYY-MM-DD 
        subdomain: String
        """
        if kwargs.has_key('state') and kwargs['state'] not in ['all', 'pending', 'in_progress', 'ended']:
            raise Exception("Invalid state parameter")
        
        if kwargs.has_key('type') and kwargs['type'] not in ['single_elimination', 'double_elimination', 'round_robin', 'swiss']:
            raise Exception("Invalid type parameter")

        response = self._call("tournaments", **kwargs)
        print "got", response
        
        target = TournamentConstructor()
        parser = XMLParser(target=target)
        parser.feed(response)
        
        return parser.close()
        
        # TODO: parse XML
    
    def create_tournament(self, tournament):
        pass


    def _call(self, request, **kwargs):
        "Generic function to send a HTTP request to Challonge."
        
        get_dict = kwargs
        get_dict['api_key'] = self.api_key
        get_string = urllib.urlencode(kwargs) if get_dict else None
        
        request_url = Challonge.CHALLONGE_BASE_URL + request + "." + self.response_format
        if get_string:
            request_url += "?" + get_string
            
        print request_url
        f = urllib2.urlopen(request_url)
        
        return f.read()
        
        


if __name__ == '__main__':
    print "Test API"
    API_KEY = "ur-key-here"
    c = Challonge(API_KEY, 'xml')
    c.get_tournaments(state='all')
    
        
    