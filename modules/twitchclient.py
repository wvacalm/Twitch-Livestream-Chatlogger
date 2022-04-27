import socket
from datetime import datetime
from dateutil import tz
from modules.authenticator import Authenticator
from modules.config import Config
from modules.logger import Logger
import time

class TwitchClient:
    _socket = socket.socket()
    _server = "irc.chat.twitch.tv" 
    _port = 6667 
    _format = "%Y-%m-%d_%H:%M:%S" 
    _is_connected = False

    # Dependencies
    _clienttoken = None
    _channeldata = None
    _logger = None
    _config = None
    _twitch_service = None

    def __init__(self, config, channel_name, redirect_uri="http://localhost:3000"):
        print("Intializing TwitchClient...")
        self._config = Config(config)
        self._redirect_uri = redirect_uri  
        self._channel_name = channel_name

        # SET UP DEPENDENCIES
        self._twitch_service = Authenticator(self._config)
        self._clienttoken = self._twitch_service.get_clienttoken()
        self._channeldata = self._twitch_service.get_channeldata(self._channel_name, self._clienttoken)
        if not self._channeldata.is_valid():
            print(f"{self._channel_name} not live!\nExiting...")
            exit()
        self._local_datetime = self.__get_datetime(self._channeldata.get_starttime())
        self._logger = Logger(self._channel_name, self._local_datetime)
        print("TwitchClient is initialized!")

    def start(self):
        self.connect()
        self.read()

    def connect(self):
        self._socket.connect((self._server, self._port))
        print(f"Connecting to: {self._server}...")
        self._socket.send(f"PASS oauth:{self._clienttoken.get_token()}\n".encode())
        self._socket.send(f"NICK {self._config.get_nickname()}\n".encode())
        self._socket.send(f"JOIN #{self._channel_name}\n".encode())
        res = self._socket.recv(4096).decode()
        print(res)
        self._is_connected = True
        title, game = self._channeldata.get_title(), self._channeldata.get_game()
        status = f"\n**TWITCH STREAM LOG**\n\"{title}\"\n{self._channel_name} has started streaming \"{game}\" at {self._local_datetime}\n"
        self._logger.log(status)

    def read(self):
        #read chat and log them
        #refresh token while client is connected to Twitch
        print(f"{datetime.now()}: Currently logging chat!\nTo watch chat in terminal run: tail -f {self._logger.get_path()}")
        while(self._is_connected):
            self.__check_refresh()
            res = self._socket.recv(4096).decode("utf-8")
            if res.startswith("PING :tmi.twitch"):
                print("PING Received")
                self._socket.send("PONG :tmi.twitch.tv\n".encode())
                print("PONG Sent")
            elif len(res) > 0:
                self._logger.log(res)
            else:
                self._is_connected = False
                print("Booted from server")
                self.reconnect()
            time.sleep(0.5)

    def disconnect(self):
        print("Disconnecting...")
        # self._socket.shutdown()
        self._socket.close()

    def reconnect(self):
        self.disconnect()
        self._clienttoken = self._twitch_service.get_clienttoken()
        self.connect()
        self.read()

    def __check_refresh(self):
        if (self._clienttoken.is_refreshable()):
            print("Refreshing Token!")
            self._clienttoken = self._twitch_service.refresh_clienttoken(self._clienttoken)

    def __get_datetime(self, starttime):
        # change UTC time to local time
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        date = starttime[ :starttime.find("T")]
        time = starttime[ starttime.find("T") + 1 : starttime.find("Z")]
        dt = datetime.strptime(date + "_" + time, self._format)
        dt = dt.replace(tzinfo=from_zone)
        dt = dt.astimezone(to_zone)
        dtstr = dt.strftime(format)
        return dtstr