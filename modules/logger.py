import logging
from emoji import demojize
from pathlib import Path

class Logger:
    def __init__(self, channel_name, datettime):
        self._channel_name = channel_name
        self._dtstr = datettime
        self._path = self.make_logpath(self._channel_name, self._dtstr)
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s — %(message)s', datefmt='%Y-%m-%d_%H:%M:%S', handlers=[logging.FileHandler(self._path, encoding='utf-8')])

    def make_logpath(self, channel_name, dtstr):
        ver = 0
        print("Creating path...")
        parent = Path("logs")
        if not parent.is_dir():
            parent.mkdir()
        parent = Path(f"logs/{channel_name}")
        if not parent.is_dir():
            parent.mkdir()
        path = Path(f"logs/{channel_name}/{dtstr}-{ver}.log")
        while path.is_file():
            ver += 1
            path = Path(f"logs/{channel_name}/{dtstr}-{ver}.log")
        return path

    def get_path(self):
        return self._path

    def log(self, msg):
        logging.info(demojize(msg))

    