
"""
All Code is written by Hippolippo and is licensed through the MIT License
"""

# A module with the purpose of syncing the apis, this will match the games from steam to a game on youtube

# Project Modules
import api_sync

# Other Modules
import json

def format_video(video: api_sync.Video_Data):
    return [video.title, video.link, video.description, video.thumbnail['url']]

def format_game(game: api_sync.Game_Data):
    playtime = game.playtime
    if playtime is None:
        playtime = "Unknown"
    elif playtime < 100:
        playtime = f"{playtime} Minutes"
    elif playtime // 60 < 100:
        playtime = f"{(playtime//6)/10} Hours"
    else:
        playtime = f"{playtime//60} Hours"
    thumbnail = game.thumbnail
    if thumbnail is None:
        thumbnail = "https://raw.githubusercontent.com/hippolippo/RCE-Games-Played-Site/master/Non-Steam.png"
    if game.last_video is not None:
        last_date = game.last_video_date.split("T")[0].split("-")
        months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "Decemebr")
        last_date = f"{months[int(last_date[1])-1]} {last_date[2]}, {last_date[0]}"
        last_video = f"https://www.youtube.com/watch?v={game.last_video}"
    else:
        last_date = "No Videos"
        last_video = None
    return [game.name, thumbnail, game.video_count, playtime, last_date, last_video]

class API_Server:
    
    def __init__(self):
        self.configs = json.load(open("api_server_config.json"))
        self.api_sync = api_sync.generate_synced_apis(self.configs["load_cached"])

    def get_games_data(self):
        games = [self.api_sync.get_game_info(self.api_sync.game_name_dict[x]) for x in self.api_sync.game_name_dict]
        games = sorted(games, key=lambda x: x.last_video_date)[::-1]
        stored_games = [game.name for game in games]
        games += sorted([self.api_sync.get_steam_info(game) for game in self.api_sync.steam_games.game_list if game.name not in stored_games], key=lambda x: x.playtime)[::-1]
        return [format_game(game) for game in games]

    def get_game_data(self, game):
        videos = self.api_sync.get_game_videos(game)
        videos = sorted(videos, key=lambda x: x.date)[::1]
        return (game, format_game(self.api_sync.get_game_info(game))[1], [format_video(video) for video in videos])

    def override_game(self, game, name, url):
        self.api_sync.youtube_game_name_dict[game].override(name, url)
        self.api_sync.__init__(self.api_sync.steam_games, self.api_sync.youtube_games, self.api_sync.non_steam_games)


if __name__ == "__main__":
    server = API_Server()
    with open("out", "w") as file:
        file.write("\n".join([x.__repr__() for x in server.get_games_data()]))
