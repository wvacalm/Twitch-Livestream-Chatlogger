class Config:
    def __init__(self, config):
        self._client_id = config["CLIENT_ID"]
        self._secret = config["SECRET"] 
        self._nickname = config["NICKNAME"]
    
    def get_client_id(self):
        return self._client_id
    
    def get_secret(self):
        return self._secret
    
    def get_nickname(self):
        return self._nickname
