from flask import Flask, jsonify, send_file
from nba_api.stats.endpoints import shotchartdetail
from matplotlib.patches import Circle, Rectangle, Arc
import matplotlib.pyplot as plt


def draw_court(ax=None, color='black', lw=2, outer_lines=False):

    if ax is None:
        ax = plt.gca()

    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)

    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color,fill=False)
    
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color,fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180,
                        linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw,
                    color=color)

    # Three point line
    # Create the side 3pt lines, they are 14ft long before they begin to arc
    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw,color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw,color=color)

    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0,linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0,linewidth=lw, color=color)
    court_elements = [hoop, backboard, outer_box, inner_box, top_free_throw,
                    bottom_free_throw, restricted, corner_three_a,
                    corner_three_b, three_arc, center_outer_arc,
                    center_inner_arc]

    if outer_lines:
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth=lw,color=color, fill=False)
        court_elements.append(outer_lines)

    for element in court_elements:
        ax.add_patch(element)

    return ax

app = Flask(__name__)


@app.route("/")
def get_player():
    lebron_data = shotchartdetail.ShotChartDetail(
    team_id=0,
    player_id=2544,
    season_type_all_star="Regular Season",
    season_nullable="2023-24",
    context_measure_simple='FGA',
    timeout=200,  # increase timeout
    headers = {
    'Host': 'stats.nba.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive'}).get_data_frames()[0]

    fig, ax = plt.subplots(figsize=(7.5,7.5))

    draw_court(ax)

    grouped = lebron_data.groupby(['EVENT_TYPE'])
    made = grouped.get_group(('Made Shot',))
    miss = grouped.get_group(('Missed Shot',))
    ax.scatter(miss['LOC_X'],miss['LOC_Y'],label='Miss',marker='x',color='tab:orange',s=30)
    ax.scatter(made['LOC_X'],made['LOC_Y'],label='Made',color='none',edgecolor='tab:blue',linewidths=1,s=30)
    plt.ylim(422.5, -47.5)
    plt.xlim(-250,250)
    plt.title('Lebron James Shot Chart - 2023-24 Season')
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelleft=False)

    ax.set_xticks([])
    ax.set_yticks([])
    plt.savefig('output.png',dpi=300)
    return send_file("output.png", mimetype='image/png')


app.run(host="0.0.0.0", port=5000)