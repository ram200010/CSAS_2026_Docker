from flask import Flask, request, send_file, render_template_string
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players
from plot_baseball_heatmap import plot_baseball_heatmap

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>CSAS 2026 - UConn</title>
</head>
<body>
    <h1>CSAS 2026 - UConn</h1>
    <h3>Plot Shot Chart of NBA Players:</h3>
    <form method="POST">
        Player Name (ex. Lebron James):
        <input name="player_id" value="Lebron James"><br><br>

        Season (ex. 2022-23):
        <input name="season" value="2022-23"><br><br>

        <input type="submit" value="Generate Plot">
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def plot():

    if request.method == "POST":
        player_name = request.form["player_id"]
        season = request.form["season"]
    else:
        return render_template_string(HTML_FORM)

    player_info = players.find_players_by_full_name(player_name)
    player_id = player_info[0]['id']
    player_name = player_info[0]['full_name']


    data = shotchartdetail.ShotChartDetail(
    team_id=0,
    player_id=player_id,
    season_type_all_star="Regular Season",
    season_nullable=season,
    context_measure_simple='FGA',
    timeout=200, 
    headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive'}).get_data_frames()[0]

    plot_baseball_heatmap(data,player_name,season)

    return send_file("output.png", mimetype='image/png')

app.run(host="0.0.0.0", port=5000)