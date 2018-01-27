
class BadStatusCode(Exception):
    ''' Exception raised if returned status code is not 200

    Attributes:
        url -- requested page
        status_code -- returned status code
    '''

    def __init__(self, url, status_code):
        self.url = url
        self.status_code = status_code
