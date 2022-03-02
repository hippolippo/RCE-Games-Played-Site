
"""
All Code is written by Hippolippo and is licensed through the MIT License
"""

class Game:

    def __init__(self, name, logo_url=None, playtime=None):
        self.name = name
        self.logo_url = logo_url
        self.playtime_forever = playtime

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

    def __repr__(self):
        return f"Generic Game \"{self.name}\" with {self.playtime_forever} minutes of playtime"

class GameList:

    # it's a list of Game Objects
    def __init__(self, game_list):
        self.game_list = []
        for i in game_list:
            if i not in self.game_list:
                self.game_list.append(i)

    # adds a game to the list of games
    def add_game(self, game: Game):
        self.game_list.append(game)

    def get_game(self, game: str):
        applicable_games = [game for game in self.game_list if game.name == game]
        if len(applicable_games) == 0: return None
        return applicable_games[0]

    # This sorts them based on the results of their get_game_playtime function
    def sorted_by_playtime(self):
        return GameList(sorted(self.game_list, key=lambda item: (item.get_game_playtime() if item.get_game_playtime() is not None else 0), reverse=True))
