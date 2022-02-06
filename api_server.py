
"""
All Code is written by Hippolippo and is licensed through the Creative Commons License
"""

# A module with the purpose of syncing the apis, this will match the games from steam to a game on youtube

# Project Modules
import api_sync

# Other Modules
import json

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
        thumbnail = """https://lh3.googleusercontent.com/yMPE-EmdX8XpV_DW6_JhIeKRssuV7VoR5Q-ufGejZR7UWUU4sC1CAbux6xnOVIW5Ibi8a4Ta8AVaj_tiwTt7rP8hFy93nQAWH-6SmDqIeZT8E-jwqXldoOTK5uY2-xAocGO9mrsR5QW2dErWwlMIADjAqO6y4HhNBMMkwMQfvjo_YmmCHtxJpuC_m9EnaQ98fuPzly6bzO6zGDs-dPSrf9q0UFYMYwrj37HZyEBCb7qri1ieUiYplgUnQaUkf9HhA37yUhOft8bokb6TkK0GxjRoBjWC0Gz965sFtCOm0Vn2A-y0Su6gJmVz4ukYvmI8N4SQ0B5910Zl_RUXSWp23FBYXMj8p0RWWcFOvVMJHvKoUwSKYXNaYwvpS8m4WoZpa2snxvmpOk_zl13kcJTkg8ihWCS-FmOyI172I4gD5dTiVBUltEGgRYXof1PcFINtRRES6cfJas5Jrbp7_H8pqGIRw_0CB6nefisnr6I4y7Q6Fj7P3w-SxS5i2xGm36j7FR4y3T105XXwCINkJPfCCzT-aCoG5R3ixJKnTTAiNPKiUSg2YkgP78p7VNOwoxiTQhrpAvW2T8vMRfREyYRrT_SFHCYa2v4pBqBpZ89Is9yZGBotL33EfM8TRWhbgFOdDsRAdauDduVLbgSjNISMz2BY1DcDDDk8bi8KlrWlz9lEFTXTO4myZkZulUOCF_EPgqx5uR-OfDRNOAmBfDxJ4cc=w184-h69-no?pageId=104482936039968502836&authuser=0"""
    last_date = game.last_video_date.split("T")[0].split("-")
    months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "Decemebr")
    last_date = f"{months[int(last_date[1])-1]} {last_date[2]}, {last_date[0]}"
    last_video = f"https://www.youtube.com/watch?v={game.last_video}"
    return [game.name, thumbnail, game.video_count, playtime, last_date, last_video]

class API_Server:
    
    def __init__(self):
        self.configs = json.load(open("api_server_config.json"))
        self.api_sync = api_sync.generate_synced_apis(self.configs["load_cached"])

    def get_games_data(self):
        games = [self.api_sync.get_game_info(self.api_sync.game_name_dict[x]) for x in self.api_sync.game_name_dict]
        games = sorted(games, key=lambda x: x.last_video_date)[::-1]
        return [format_game(game) for game in games]

    def get_game_data(self, game):
        pass


if __name__ == "__main__":
    server = API_Server()
    with open("out", "w") as file:
        file.write("\n".join([x.__repr__() for x in server.get_games_data()]))
