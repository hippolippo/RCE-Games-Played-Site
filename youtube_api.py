
"""
All Code is written by Hippolippo and is licensed through the Creative Commons License
"""

# A module to serve the purpose of gathering data about the videos made by a channel

# Project Modules
import generic

# Other Modules
import requests
import json
import re

# Youtube API Key. Do Not Share
API_KEY = ""
# The id of the channel that this will be applied to (RCE)
CHANNEL_ID = "UCeP4Yv3s4RvS0-6d9OInRMw"

class YoutubeGame(generic.Game):

    videos = []

    def add_video(self, video):
        self.videos.append(video)

    def list_videos(self):
        return self.videos

class YoutubeGameList(generic.GameList):

    def append(self, game):
        self.game_list.append(game)


class YoutubeVideo:
    
    def __init__(self, json):
        print("-")
        self.id = json["id"]["videoId"]
        self.gameName = self.get_game_name()
        self.game = initialize_game(self.gameName, self)
        self.title = json["snippet"]["title"]
        print("|")

    def get_game_name(self):
        overrides = json.load(open("video_game_override.json", "r"))["videos"]
        if self.id in overrides:
            return overrides[self.id]
        cache = json.load(open("video_game_cache.json", "r"))
        if self.id in cache:
            game_name = cache[self.id]
        else:
            request = requests.get(f"https://www.youtube.com/watch?v={self.id}")
            game_name = re.findall("""(?<=,"title":\{"simpleText":").*?(?="},"subtitle")""", request.content.decode("utf-8"))[0].split("\"}")[0]
            cache[self.id] = game_name
            with open("video_game_cache.json", "w") as file:
                json.dump(cache, file)
        overrides = json.load(open("video_game_override.json", "r"))["games"]
        if game_name in overrides:
            return overrides[game_name]
        else:
            return game_name

YoutubeGames = YoutubeGameList([]);

def initialize_game(gameName, video):
    global YoutubeGames
    if True not in [gameName == game.get_game_name() for game in YoutubeGames.game_list]:
        YoutubeGames.append(YoutubeGame(gameName))
    game = YoutubeGames.game_list[[gameName == game.get_game_name() for game in YoutubeGames.game_list].index(True)]
    game.add_video(video)
    return game

# Make a request to a specific api path including the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request(path, flags=[]):
    request = requests.get("https://www.googleapis.com/youtube/v3" + path + "?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&".join([""] + flags))
    if request.status_code == 200:
        print("suc")
        return request.json()
    print(request.json())


# Make a request to a specific api path without the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request_general(path, flags=[]):
    request = requests.get("https://www.googleapis.com/youtube/v3" + path + "?key=" + API_KEY  + "&".join([""] + flags))
    if request.status_code == 200:
        return request.json()

def get_all_videos():
    items = []
    result = json_request("/search", ["order=date","part=snippet","type=video","max_results=50"])
    items += result["items"]
    while "nextPageToken" in result:
        result = json_request("/search", ["order=date","part=snippet","type=video","max_results=50", f"pageToken={result['nextPageToken']}"])
        items += result["items"]
    return items
        
"""with open("stuff", "w") as file:
    videos = get_all_videos()
    print(YoutubeVideo(videos[1]).gameName)
    json.dump(videos, file)"""
"""
vids = get_all_videos()
with open("stuff", "w") as file:
    json.dump(vids, file)
"""
with open("stuff", "r") as file:
    vids = json.load(file)
videos = [YoutubeVideo(vid) for vid in vids]
print([item.get_game_name() for item in YoutubeGames.game_list])