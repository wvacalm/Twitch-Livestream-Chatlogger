class TwitchChannel:

    _valid = False
    def __init__(self, data):
        if data:
            self._valid = True
            self._title = data["title"]
            self._game = data["game_name"]
            self._type = data["type"]
            self._starttime = data["started_at"]
    
    def get_title(self):
        return self._title if self._valid else None
    
    def get_game(self):
        return self._game if self._valid else None
    
    def get_starttime(self):
        return self._starttime if self._valid else None

    def is_live(self):
        status = True if self._type else False
        return status if self._valid else None
    
    def is_valid(self):
        return self._valid
    

        
