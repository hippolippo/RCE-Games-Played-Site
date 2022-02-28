from jinja2 import Template
import api_server

server = api_server.API_Server()
t = Template(open("Exported Html/index.html").read())
with open("out.html", "w") as file:
    file.write(t.render(games=server.get_games_data()))