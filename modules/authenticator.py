import random
import string
import webbrowser
import requests 
from requests.structures import CaseInsensitiveDict
from modules.clienttoken import ClientToken
from modules.twitchchannel import TwitchChannel

class Authenticator:
    # twitch service
    _auth_rtoken = None
    def __init__(self, client_id, client_secret, redirect_uri="http://localhost:3000"):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._auth_code = self.__get_authcode()

    def __state(self, n):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(n))
    def get_authcode(self):
        return self._auth_code

    def __get_authcode(self): 
        state = self.__state(15)
        print(f"Input State: {state} \n")
        url = f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self._client_id}&redirect_uri={self._redirect_uri}&scope=chat%3Aread&state={state}"
        webbrowser.open(url)
        print("Enter URL From Browser: ")
        auth_url = input()
        res_state = auth_url[auth_url.find("&state=") + len("&state=") : ]
        if state != res_state:
            print("STATES DO NOT MATCH")
            exit()
        prefixSpot = auth_url.find("?code=")
        postfixSpot = auth_url.find("&scope=")
        auth_code = auth_url[prefixSpot + len("?code=") : postfixSpot]
        return auth_code

    def refresh_clienttoken(self, auth_rtoken):
        url = "https://id.twitch.tv/oauth2/token"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = f"grant_type=refresh_token&refresh_token={auth_rtoken}&client_id={self._client_id}&client_secret={self._client_secret}"
        res = requests.post(url, headers=headers, data=data)
        res = res.json()
        auth_token = res["access_token"]
        self._auth_rtoken = res["refresh_token"] 
        token_lifetime = res["expires_in"] 
        clienttoken = ClientToken(auth_token, self._auth_rtoken, token_lifetime)
        return clienttoken

    def get_clienttoken(self):
        url = "https://id.twitch.tv/oauth2/token"
        headers = CaseInsensitiveDict()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        data = f"client_id={self._client_id}&client_secret={self._client_secret}&code={self._auth_code}&grant_type=authorization_code&redirect_uri=http://localhost:3000"
        res = requests.post(url, headers=headers, data=data)
        res = res.json()
        auth_token = res["access_token"] 
        self._auth_rtoken = res["refresh_token"] 
        token_lifetime = res["expires_in"] 
        clienttoken = ClientToken(auth_token, self._auth_rtoken, token_lifetime)
        return clienttoken

    def get_channeldata(self, channel_name, auth_token):
        url = f"https://api.twitch.tv/helix/streams?user_login={channel_name}"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = f"Bearer {auth_token}"
        headers["Client-Id"] = f"{self._client_id}"
        res = requests.get(url, headers=headers).json()
        unfiltered_data = res["data"][0] if res["data"] else res["data"]
        channeldata = TwitchChannel(unfiltered_data)
        return channeldata

