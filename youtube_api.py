
"""
All Code is written by Hippolippo and is licensed through the MIT License
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

    def __init__(self, name, logo_url=None, playtime=None, original_name=None):
        self.original_name = original_name if original_name is not None else name;
        super().__init__(name, logo_url, playtime)
        self.videos = []

    def add_video(self, video):
        self.videos.append(video)

    def list_videos(self):
        return self.videos

    def override(self, name, url):
        overrides = {}
        with open("video_game_override.json", "r") as file:
            overrides = json.load(file)
        overrides["games"][self.original_name] = [name, url]
        with open("video_game_override.json", "w") as file:
            json.dump(overrides, file)
        self.name = name

    def __repr__(self):
        return f"Youtube Game \"{self.get_game_name()}\" with {len(self.videos)} videos"

class YoutubeGameList(generic.GameList):

    def append(self, game):
        self.game_list.append(game)
        


class YoutubeVideo:
    
    def __init__(self, json):
        self.id = json["id"]["videoId"]
        temp = self.get_game_name()
        self.gameName = temp[0]
        self.originalGameName = temp[1]
        self.game = initialize_game(self.gameName, self, original_name=self.originalGameName)
        self.title = json["snippet"]["title"]
        self.thumbnail = json["snippet"]["thumbnails"]["high"]
        self.date = json["snippet"]["publishTime"]
        self.description = json["snippet"]["description"]

    @property
    def link(self):
        return f"https://www.youtube.com/watch?v={self.id}"
        

    def get_game_name(self):
        overrides = json.load(open("video_game_override.json", "r"))["videos"]
        if self.id in overrides:
            return overrides[self.id]
        cache = json.load(open("video_game_cache.json", "r"))
        if self.id in cache:
            game_name = cache[self.id]
        else:
            print(f"Downloading game name for video with id {self.id}")
            request = requests.get(f"https://www.youtube.com/watch?v={self.id}")
            game_name = re.findall("""(?<=,"title":\{"simpleText":").*?(?="},"subtitle")""", request.content.decode("utf-8"))[0].split("\"}")[0]
            print(f"Found: {game_name}")
            cache[self.id] = game_name
            with open("video_game_cache.json", "w") as file:
                json.dump(cache, file)
        overrides = json.load(open("video_game_override.json", "r"))["games"]
        if game_name in overrides:
            return overrides[game_name][0], game_name
        else:
            return game_name, game_name
    
    def __repr__(self):
        return self.id
    

YoutubeGames = YoutubeGameList([]);

def initialize_game(gameName, video, original_name=None):
    global YoutubeGames
    if True not in [gameName == game.get_game_name() for game in YoutubeGames.game_list]:
        YoutubeGames.append(YoutubeGame(gameName, original_name=original_name))
    game = YoutubeGames.game_list[[gameName == game.get_game_name() for game in YoutubeGames.game_list].index(True)]
    game.add_video(video)
    return game

# Make a request to a specific api path including the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request(path, flags=[]):
    print(f"making request to {path} with flags {flags}")
    request = requests.get("https://www.googleapis.com/youtube/v3" + path + "?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&".join([""] + flags))
    if request.status_code == 200:
        return request.json()


# Make a request to a specific api path without the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request_general(path, flags=[]):
    print(f"making request to {path} with flags {flags}")
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
    with open("video_data_cache.json", "w") as file:
        json.dump(sorted(items,key= lambda x: x["snippet"]["publishTime"]), file)
    return sorted(items,key= lambda x: x["snippet"]["publishTime"])

def update_videos(current_list):
    result = json_request("/search", ["order=date","part=snippet","type=video","max_results=10"])
    amount_added = 0
    for i in result["items"]:
        print(i['id']['videoId']+":", i['snippet']['title'])
        if i['id']['videoId'] not in [item['id']['videoId'] for item in current_list]:
            amount_added += 1
            current_list.append(i)
            print(i)
    while amount_added >= 10 and "nextPageToken" in result:
        result = json_request("/search", ["order=date","part=snippet","type=video","max_results=10", f"pageToken={result['nextPageToken']}"])
        amount_added = 0
        for i in result["items"]:
            if i['id']['videoId'] not in [item['id']['videoId'] for item in current_list]:
                amount_added += 1
                current_list.append(i)
                print(i)
    return current_list

def load_videos_from_cache():
    with open("video_data_cache.json", "r") as file:
        vids = json.load(file)
    vids = sorted(vids, key= lambda x: x["snippet"]["publishTime"])
    return vids
    
