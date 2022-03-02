from flask import Flask, render_template, request, redirect, session, url_for
import api_server
import random
import json

letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890-=!@#$%^&*()_+<>?:{}|,./;[]"
key = "".join([random.choice(letters) for i in range(75)])

app = Flask(__name__, template_folder="templates", static_folder="assets")
api = api_server.API_Server()

app.config.update({
    'SECRET_KEY': key
})

@app.route('/')
def index():
    if "admin" not in session: session["admin"] = False
    return render_template('index.html', games=api.get_games_data(), admin=session["admin"])

@app.route('/game')
def game():
    if "admin" not in session: session["admin"] = False
    game = request.args.get('game')
    data = api.get_game_data(game)
    return render_template('game.html', videos=data[2], game=data[0], logo=data[1], admin=session["admin"])

@app.route('/socials')
def socials():
    if "admin" not in session: session["admin"] = False
    return render_template('socials.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if "admin" not in session: session["admin"] = False
    if request.method == 'GET':
        return render_template("login.html")
    if request.method == 'POST':
        if request.form['password'] == "password":
            session["admin"] = True
            return redirect(url_for('admin'))
        else:
            session["admin"] = False
            return render_template("login.html", error="invalid password")

@app.route('/admin')
def admin():
    if "admin" not in session: session["admin"] = False
    if session["admin"]:
        return redirect(url_for('index'))
    return redirect(url_for('login'))

@app.route('/editgame', methods=['GET', 'POST'])
def editgame():
    if "admin" not in session: session["admin"] = False
    if not session["admin"]:
        return redirect(url_for("index"))
    game = request.args.get('game')
    if request.method == 'GET':
        return render_template("editgame.html", game = game)
    if request.method == 'POST':
        api.override_game(request.form["game"], request.form["name"], request.form["url"])
        return redirect(url_for('game') + f'?game={request.form["name"]}')