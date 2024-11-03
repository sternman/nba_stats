import streamlit as st
import pandas as pd
import nba_api
from nba_api.stats.endpoints import playercareerstats

from nba_api.stats.endpoints import commonplayerinfo, commonallplayers

st.set_page_config(layout="wide")

st.write("# NBA Stats")


from nba_api.stats.static import players
seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", '2023-24', "2024-25"]
leagues = ["00"]
isCurrentSeasonOnly = 0

season = st.selectbox("Select Season", seasons, index=6)
if season:
    season_years = season.split("-")
    start_year = int(season_years[0])
    end_year = int(f"20{season_years[1]}")
    # st.write(start_year, end_year)
    players = commonallplayers.CommonAllPlayers(is_only_current_season=isCurrentSeasonOnly, league_id=leagues[0], season=season)
    # st.write(dir(players))
    cur_players = [f"{x[2]}-{x[0]}" for x 
                   in players.get_dict()["resultSets"][0]["rowSet"]  
                   if start_year >=int(x[4])
                   and start_year <= int(x[5])
                   ]
    cur_players = sorted(cur_players)
    # st.write(len(cur_players))
# Get all players
# players = players.get_players()
    selected_player = st.selectbox("Select Player", cur_players)
    if selected_player:
        player_id = selected_player.split("-")[1]
        player_name = selected_player.split("-")[0]

        # Nikola Jokić
        career = playercareerstats.PlayerCareerStats(player_id=player_id) 

        # pandas data frames (optional: pip install pandas)
        st.write(career.get_data_frames()[0])

        # json
        # st.write(career.get_json())

        # dictionary
        # st.write(career.get_dict())
    # st.write(dir(nba_api))
