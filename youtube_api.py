
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
    pass
class YoutubeGameList(generic.GameList):
    pass

class YoutubeVideo:
    
    def __init__(self, json):
        self.id = json["id"]["videoId"]
        self.gameName = self.get_game_name()
        self.title = json["snippet"]["title"]

    def get_game_name(self):
        request = requests.get(f"https://www.youtube.com/watch?v={self.id}")
        return re.findall("""(?<=,"title":\{"simpleText":").*?(?="},"subtitle")""", request.content.decode("utf-8"))[0].split("\"},\"callToAction")[0]

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

def get_game_name(id):
    request = requests.get(f"https://www.youtube.com/watch?v={id}")
    return re.findall("""(?<=,"title":\{"simpleText":").*?(?="},"subtitle")""", request.content.decode("utf-8"))[0].split("\"},\"callToAction")[0]

print(get_game_name("Ry9SXNCkwuk"))
