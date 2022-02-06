
"""
All Code is written by Hippolippo and is licensed through the Creative Commons License
"""

class Game:

    def __init__(self, name, logo_url=None, playtime=None):
        self.name = name
        self.logo_url = logo_url
        self.playtime = playtime

    # Get url for the game's logo image
    def get_logo_url(self) -> str:
        if self.logo_url is None:
            return None
        return self.logo_url

    # Get the display name of the game
    def get_game_name(self) -> str:
        if(self.name is None):
            return None
        return self.name

    # Get the number of minutes the game was played
    def get_game_playtime(self) -> int:
        if(self.playtime_forever is None):
            return None
        return self.playtime_forever

class GameList:

    # it's a list of Game Objects
    def __init__(self, game_list):
        self.game_list = game_list

    # adds a game to the list of games
    def add_game(self, game: Game):
        self.game_list.append(game)

    # This sorts them based on the results of their get_game_playtime function
    def sorted_by_playtime(self):
        return GameList(sorted(self.game_list, key=lambda item: (item.get_game_playtime() if item.get_game_playtime() is not None else 0), reverse=True))
