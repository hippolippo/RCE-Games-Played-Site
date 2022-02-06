
"""
All Code is written by Hippolippo and is licensed through the Creative Commons License
"""

# A module with the purpose of syncing the apis, this will match the games from steam to a game on youtube

# Project Modules
import steam_api
import youtube_api
import generic

# Other Modules
import json

class Video_Data:
    game = None
    thumbnail = None
    title = None
    date = None

class Game_Data:
    name = None
    thumbnail = None
    video_count = None
    playtime = None
    last_video_date = None
    last_video = None

    def __repr__(self):
        return f"Game Data: {self.name}, {self.video_count} videos, {self.playtime} minutes played, last video released {self.last_video_date}, recent video id: {self.last_video}"

class API_Syncer:

    def __init__(self, steam_games: steam_api.SteamGameList, youtube_games: youtube_api.YoutubeGameList, non_steam_games: generic.GameList):
        self.game_dict: dict[youtube_api.YoutubeGame, generic.Game] = dict()
        for game in youtube_games.game_list:
            steam_overlap = [steam_game for steam_game in steam_games.game_list if steam_game.name == game.name]
            non_steam_overlap = [non_steam_game for non_steam_game in non_steam_games.game_list if non_steam_game.name == game.name]
            if len(steam_overlap) > 0:
                self.game_dict[game] = steam_overlap[0]
            elif len(non_steam_overlap) > 0:
                self.game_dict[game] = non_steam_overlap[0]
            else:
                new_game = generic.Game(game.name)
                non_steam_games.add_game(new_game)
                self.game_dict[game] = new_game
        self.reverse_game_dict: dict[generic.Game, youtube_api.YoutubeVideo] = {self.game_dict[item]: item for item in self.game_dict}
        self.game_name_dict: dict[str, generic.Game] = {game.get_game_name(): self.game_dict[game] for game in self.game_dict}
        self.youtube_game_name_dict: dict[str, youtube_api.YoutubeGame] = {game.get_game_name(): game for game in self.game_dict}
    
    def get_video_data(self, video: youtube_api.YoutubeVideo):
        data = Video_Data()
        data.game = self.game_dict[video.game]
        data.thumbnail = video.thumbnail
        data.title = video.title
        data.date = video.date
        return data
    
    def get_game_from_name(self, game_name):
        return self.game_name_dict[game_name]

    def get_youtube_game_from_name(self, game_name):
        return self.youtube_game_name_dict[game_name]

    def get_game_videos(self, game):
        if type(game) is str:
            game = self.get_youtube_game_from_name(game)
        if type(game) is not youtube_api.YoutubeGame:
            game = self.reverse_game_dict[game]
        video_list = game.videos
        return video_list

    def get_game_info(self, game):
        if type(game) is str:
            game = self.get_game_from_name(game)
        if type(game) is youtube_api.YoutubeGame:
            game = self.game_dict[game]
        video_list = self.reverse_game_dict[game].videos
        game_data = Game_Data()
        game_data.name = game.get_game_name()
        game_data.thumbnail = game.get_logo_url()
        game_data.video_count = len(video_list)
        game_data.playtime = game.get_game_playtime()
        game_data.last_video = sorted(self.reverse_game_dict[game].videos, key = lambda x: x.date)[-1]
        game_data.last_video_date = game_data.last_video.date
        return game_data

if __name__ == "__main__":
    print("Running Tests for API Sync")
    vids = youtube_api.load_videos_from_cache()
    vids = [youtube_api.YoutubeVideo(vid) for vid in vids]
    steam_games = steam_api.generate_steamgamelist()
    non_steam = generic.GameList([])
    synced = API_Syncer(steam_games, steam_api.SteamGameList([vid.game for vid in vids]), non_steam)
    print(synced.get_game_info("Poly Bridge 2"))
    print(synced.get_game_videos("Poly Bridge 2"))
    print(synced.get_youtube_game_from_name("Poly Bridge 2"))
    print(synced.get_game_from_name("Poly Bridge 2"))