import requests

API_KEY = ""
USER_ID = "76561198333972976"

class Game:

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

class GameList:

    def __init__(self, game_list):
        self.game_list = game_list

    def sorted_by_playtime(self):
        return GameList(sorted(self.game_list, key=lambda list: list.playtime_forever, reverse=True))

def json_request(path, flags=[]):
    request = requests.get("http://api.steampowered.com" + path+"?key=" + API_KEY + "&steamid=" + USER_ID + "&".join([""] + flags) + "&format=json")
    if request.status_code == 200:
        return request.json()

def json_request_general(path, flags=[]):
    request = requests.get("http://api.steampowered.com" + path+"?key=" + API_KEY  + "&".join([""] + flags) + "&format=json")
    if request.status_code == 200:
        return request.json()

def get_logo_url(game: Game):
    if(game.appid is None or game.img_logo_url is None):
        return None
    return "http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{hash}.jpg".format(appid=game.appid, hash=game.img_logo_url)

def generate_gamelist():
    data = json_request("/IPlayerService/GetOwnedGames/v0001/", ["include_appinfo=true"])
    game_data = data['response']['games']
    games = [Game(info) for info in game_data]
    game_list = GameList(games)
    return game_list

