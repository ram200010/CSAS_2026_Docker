from nba_api.stats.endpoints import shotchartdetail
import pandas as pd

def get_data(player_id,target_season):

    features = ["PERIOD", "MINUTES_REMAINING","SECONDS_REMAINING","ACTION_TYPE",
    "SHOT_TYPE","SHOT_ZONE_BASIC","SHOT_ZONE_AREA","SHOT_ZONE_RANGE","SHOT_DISTANCE",
    "LOC_X", "LOC_Y", "HTM", "VTM", "TEAM_NAME","SHOT_MADE_FLAG"]

    end_year = int(target_season[:4]) 

    seasons = [f"{y}-{str(y+1)[-2:]}" for y in range(end_year - 5, end_year)]

    all_data = []

    for season in seasons:

        print(f"Fetching {season}...")

        df = shotchartdetail.ShotChartDetail(
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


        df = df[features]
        df["SEASON"] = season
        all_data.append(df)

    train_data = pd.concat(all_data, ignore_index=True)

    print(f"Fetching {target_season}...")

    test_data = shotchartdetail.ShotChartDetail(
                    team_id=0,
                    player_id=player_id,
                    season_type_all_star="Regular Season",
                    season_nullable=target_season,
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
    
    return train_data, test_data
        

    


