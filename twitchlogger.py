import socket
import logging
import time
import datetime
from datetime import timedelta
from emoji import demojize
from utility import *
from manip import *
class TwitchLogger:
    _socket = socket.socket()
    _server = "irc.chat.twitch.tv"
    _port = 6667
    _format = "%Y-%m-%d_%H:%M:%S"

    def __init__(self, config, channel, redirect_uri="http://localhost:3000"):
        print("Intializing TwitchLogger...")
        self._client_id = config["CLIENT_ID"]
        self._secret = config["SECRET"]
        self._nickname = config["NICKNAME"]
        self._redirect_uri = redirect_uri
        self._channel = channel

        # COMMUNICATE WITH TWITCH API
        self._auth_code = get_authcode(self._client_id, self._redirect_uri)
        auth_res = get_authtoken(self._client_id, self._secret, self._auth_code)
        self._auth_token = auth_res["access_token"]
        self._auth_rtoken = auth_res["refresh_token"]
        token_lifetime = auth_res["expires_in"]
        self._lsdata = get_lsdata(self._channel, self._client_id, self._auth_token)
        # self._expires_in = datetime.now() + timedelta(seconds=token_lifetime)
        self._token_lifetime = datetime.now()
        stype = self._lsdata["type"]

        if not stype:
            print(f"{self._channel} not live!\nExiting...")
            exit()
        self.logsetup()
        self.connect()
        self.logit()

    def logsetup(self):
        if self._lsdata:
            self._dtstr = get_datetime(self._lsdata["started_at"])
            self._path = make_logpath(self._channel, self._dtstr)
            logging.basicConfig(level=logging.DEBUG,format='%(asctime)s — %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', handlers=[logging.FileHandler(self._path, encoding='utf-8')])
            print(f"File has been created at: {self._path}")
        else: 
            print("Could not set up logging")
            exit()

    def connect(self):
        self._socket.connect((self._server, self._port))
        print(f"Connecting to: {self._server}...")
        self._socket.send(f"PASS oauth:{self._auth_token}\n".encode())
        self._socket.send(f"NICK {self._nickname}\n".encode())
        self._socket.send(f"JOIN #{self._channel}\n".encode())
        res = self._socket.recv(2048).decode()
        print(res)
        stitle = self._lsdata["title"]
        sgame = self._lsdata["game_name"]
        status = f"\n**TWITCH STREAM LOG**\n\"{stitle}\"\n{self._channel} has started streaming \"{sgame}\" at {self._dtstr}\n"
        print(status)
        logging.info(status)
    
    def tkexpired(self):
        return datetime.now() > self._expires_in
        
    def logit(self):
        print(f"Currently logging chat!\nTo watch chat in terminal run: tail -f {self._path}")
        while(True):
            res = self._socket.recv(2048).decode()
            if res.startswith("PING :tmi.twitch"):
                print("PING Received")
                self._socket.send("PONG :tmi.twitch.tv\n".encode())
                print("PONG Sent")
            elif len(res) > 0:
                logging.info(demojize(res))
            else:
                print(f"Reading Nothing! Attempting to Reconnect!")
                if (self.tkexpired()):
                    self.connect(self._auth_token)
            if (datetime.now() - self._token_lifetime).total_seconds() > 2700 : 
                refresh_res = refresh_authtoken(self._client_id, self._secret, self._auth_rtoken)
                self._auth_token = refresh_res["access_token"]
                self._auth_rtoken = refresh_res["refresh_token"]
            time.sleep(0.2) 


    