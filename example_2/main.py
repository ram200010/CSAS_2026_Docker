
from nba_api.stats.static import players
from get_data import get_data
from model import train_rf_shot_model


player_name = input('Enter NBA Player Name: ')
player_season = input('Enter Season to be Predicted: ')

player_info = players.find_players_by_full_name(player_name)
player_id = player_info[0]['id']
player_name = player_info[0]['full_name']

print('Gathering data for ',player_name)

train_data, test_data = get_data(player_id,player_season)

print(train_data.head())

print('Training Random Forest Model')



train_rf_shot_model(train_data,test_data)
