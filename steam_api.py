
"""
All Code is written by Hippolippo and is licensed through the MIT License
"""

# A module to serve the purpose of gathering games from the steam api

# Project Modules
import generic

# Other Modules
import requests

# Steam API key. Do Not Share
API_KEY = "A908ED00E26D38151C195B78C8FE179D"
# The id of the user that this will be applied to (RCE)
USER_ID = "76561198333972976"

# An object describing the properties of a game on steam
class SteamGame(generic.Game):

    def __init__(self, gamedata):
        self.appid = gamedata['appid']  if 'appid' in gamedata else None
        self.name = gamedata['name']  if 'name' in gamedata else None
        self.playtime_forever = gamedata['playtime_forever'] if 'playtime_forever' in gamedata else None
        self.img_icon_url = gamedata['img_icon_url'] if 'img_icon_url' in gamedata else None
        self.img_logo_url = gamedata['img_logo_url'] if 'img_logo_url' in gamedata else None
        self.has_community_visible_stats = gamedata['has_community_visible_stats'] if 'has_community_visible_stats' in gamedata else None
        self.playtime_windows_forever = gamedata['playtime_windows_forever'] if 'playtime_windows_forever' in gamedata else None
        self.playtime_mac_forever = gamedata['playtime_mac_forever'] if 'playtime_mac_forever' in gamedata else None
        self.playtime_linux_forever = gamedata['playtime_linux_forever'] if 'playtime_linux_forever' in gamedata else None

    # Get url for the game's logo image
    def get_logo_url(self) -> str:
        if(self.appid is None or self.img_logo_url is None):
            return None
        return "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(appid=self.appid, hash=self.img_logo_url)
    
    def __repr__(self):
        return f"Steam Game \"{self.name}\" with {self.playtime_forever} minutes of playtime"

# An object describing a list of SteamGame Objects with methods to return the list sorted
class SteamGameList(generic.GameList):

    def sorted_by_playtime(self):
        return SteamGameList(sorted(self.game_list, key=lambda item: (item.get_game_playtime() if item.get_game_playtime() is not None else 0), reverse=True))


# Make a request to a specific api path including the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request(path, flags=[]):
    request = requests.get("http://api.steampowered.com" + path + "?key=" + API_KEY + "&steamid=" + USER_ID + "&".join([""] + flags) + "&format=json")
    if request.status_code == 200:
        return request.json()

# Make a request to a specific api path without the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request_general(path, flags=[]):
    request = requests.get("http://api.steampowered.com" + path + "?key=" + API_KEY  + "&".join([""] + flags) + "&format=json")
    if request.status_code == 200:
        return request.json()

# Creates a SteamGameList object by finding the games owned by the user
def generate_steamgamelist() -> SteamGameList:
    data = json_request("/IPlayerService/GetOwnedGames/v0001/", ["include_appinfo=true"])
    game_data = data['response']['games']
    games = [SteamGame(info) for info in game_data]
    game_list = SteamGameList(games)
    return game_list


if __name__ == "__main__":
    print([(game.get_logo_url(), game.img_icon_url) for game in generate_steamgamelist().game_list if game.name == "Poly Bridge 2"])
    #print([(game.name, game.appid) for game in generate_steamgamelist().sorted_by_playtime().game_list])
