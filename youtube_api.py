
"""
All Code is written by Hippolippo and is licensed through the Creative Commons License
"""

# A module to serve the purpose of gathering data about the videos made by a channel

# Project Modules
import generic

# Other Modules
import requests
import json

# Youtube API Key. Do Not Share
API_KEY = ""
# The id of the channel that this will be applied to (RCE)
CHANNEL_ID = "UCeP4Yv3s4RvS0-6d9OInRMw"

# Make a request to a specific api path including the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request(path, flags=[]):
    request = requests.get("https://www.googleapis.com/youtube/v3" + path + "?key=" + API_KEY + "&channelId=" + CHANNEL_ID + "&".join([""] + flags))
    if request.status_code == 200:
        return request.json()


# Make a request to a specific api path without the user id
# DO NOT PUT USER INPUT INTO THE PARAMETERS OF THIS METHOD
def json_request_general(path, flags=[]):
    request = requests.get("https://www.googleapis.com/youtube/v3" + path + "?key=" + API_KEY  + "&".join([""] + flags))
    if request.status_code == 200:
        return request.json()

with open("stuff", "w") as file:
    json.dump(json_request("/search", ["order=date","part=snippet","type=video","max_results=50"]), file)