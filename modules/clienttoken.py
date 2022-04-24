import datetime

class ClientToken:
    # encapsulate token detail
    def __init__(self, auth_token, auth_rtoken, expires_in):
        self._auth_token = auth_token 
        self._auth_rtoken = auth_rtoken 
        self._expires_in = expires_in 
        self._birth_date = datetime.datetime.now()
    
    def get_token(self):
        return self._auth_token
    
    def get_retoken(self):
        return self._auth_rtoken
    
    def get_expirydate(self):
        # get the time this token expires
        return self._birth_date + datetime.timedelta(seconds=self._expires_in)

    def get_lifetime(self):
        return self._birth_date + datetime.datetime.now()
        
    def is_expired(self):
        expiry_date = self.get_expirydate()
        return datetime.datetime.now() > expiry_date
    
    def is_refreshable(self):
        refresh_time = self.get_expirydate() - datetime.timedelta(seconds=300)
        return datetime.datetime.now() > refresh_time
