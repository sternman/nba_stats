import streamlit as st
import pandas as pd
import nba_api
from datetime import datetime, timedelta

from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
# from nba_api.stats.static import players

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2
from nba_api.stats.endpoints.boxscorescoringv2 import BoxScoreScoringV2
from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
st.set_page_config(layout="wide")
game_date = datetime.now()-timedelta(hours=5)
game_date = game_date.strftime("%A, %B %d, %Y")


st.write("# NBA Live Stats")
st.write(f"## _{game_date}_")



head_shot_url = "https://cdn.nba.com/headshots/nba/latest/260x190/"


seasons = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", '2023-24', "2024-25"]
leagues = ["00"]
isCurrentSeasonOnly = 0

# season = st.selectbox("Select Season", seasons, index=6)

# if season:
    # season_years = season.split("-")
    # start_year = int(season_years[0])
dt_start = datetime.now()-timedelta(hours=5)
dt_start = dt_start.strftime("%Y-%m-%d")
dt_end = datetime.now() + timedelta(days=1) - timedelta(hours=5)
dt_end = dt_end.strftime("%Y-%m-%d")
# end_year = int(f"20{season_years[1]}")
# st.write(dir(LeagueGameLog))
game_log = None
game_log = LeagueGameLog(season="2024-25", league_id=leagues[0], date_from_nullable=dt_start, date_to_nullable=dt_end)
# st.write(data.get_dict())
games = game_log.get_dict()["resultSets"][0]["rowSet"]
games_list = []
for game in games:
    game_id = game[4]
    team = game[3]
    teamid = game[1]
    
    games_list.append((game_id, team, teamid))

game_ids = set([x[0] for x in games_list])

todays_games = []
for game_id in game_ids:
    team1 = [x[1] for x in games_list if x[0] == game_id][0]
    team2 = [x[1] for x in games_list if x[0] == game_id][1]
    todays_games.append(f"{team1} vs. {team2} - {game_id}")


selected_game = st.selectbox("Select Game", todays_games)

if "scoreboard" not in st.session_state:
    scoreBoard = ScoreboardV2(game_date=dt_start, league_id=leagues[0])
    st.session_state.scoreboard = scoreBoard  

if "scoreboard" in st.session_state:
    scoreBoard = ScoreboardV2(game_date=dt_start, league_id=leagues[0])
    st.session_state.scoreboard = scoreBoard  

# data_2 = ScoreboardV2(game_date=dt_start, league_id=leagues[0])
# st.write(data_2.get_dict())


if selected_game:
    # st.write(selected_game)
    lookup_gameid = selected_game.split(" - ")[1]
    team1 = selected_game.split(" - ")[0].split(" vs. ")[0]
    team2 = selected_game.split(" - ")[0].split(" vs. ")[1]
    # st.write(f"{team1} vs. {team2}")
    teamid1 = [x[2] for x in games_list if x[0] == lookup_gameid][0]
    teamid2 = [x[2] for x in games_list if x[0] == lookup_gameid][1]
    # st.write(teamid1, teamid2)

    bx = None
    bxs = None
    scoreBoard = None

    bx = BoxScoreScoringV2(game_id=lookup_gameid )
    bxs = BoxScoreSummaryV2(game_id=lookup_gameid )
    
    scoreBoard = st.session_state.scoreboard

    scoreBoardHeader = scoreBoard.get_data_frames()[0]
    scoreBoardLineScore = scoreBoard.get_data_frames()[1]

    gameHeader = scoreBoardHeader[scoreBoardHeader["GAME_ID"] == lookup_gameid]
    gameLineScore = scoreBoardLineScore[scoreBoardLineScore["GAME_ID"] == lookup_gameid]

    
    time = gameHeader["LIVE_PC_TIME"].values[0]
    quarter = gameHeader["LIVE_PERIOD"].values[0]
    arena = gameHeader["ARENA_NAME"].values[0]
    homeBroadcast = gameHeader["HOME_TV_BROADCASTER_ABBREVIATION"].values[0]
    awayBroadcast = gameHeader["AWAY_TV_BROADCASTER_ABBREVIATION"].values[0]
    

    players_stats = bx.get_data_frames()[0]
    # st.write(players_stats)
    team1_stats = players_stats[players_stats["TEAM_ID"] == teamid1]
    team2_stats = players_stats[players_stats["TEAM_ID"] == teamid2]
    # team1_starters = team1_stats[team1_stats["START_POSITION"] != ""]
    # team2_starters = team2_stats[team2_stats["START_POSITION"] != ""]
    team1_starters = team1_stats
    team2_starters = team2_stats
    # st.write(team1_starters)
    team1_starters_condensed = team1_starters[["PLAYER_NAME", "START_POSITION", "PLAYER_ID", "COMMENT"]]
    team2_starters_condensed = team2_starters[["PLAYER_NAME", "START_POSITION", "PLAYER_ID", "COMMENT"]]

    
    
    #head shot url
    #https://cdn.nba.com/headshots/nba/latest/260x190/1628369.png
    
    # team1_stats = bx.get_data_frames()[1]
    linescores = bxs.get_data_frames()[5]
    team1_linescores = linescores[linescores["TEAM_ID"] == teamid1].values[0]
    team2_linescores = linescores[linescores["TEAM_ID"] == teamid2].values[0]
    


    team1_q1_pts = team1_linescores[8]
    team1_q2_pts = team1_linescores[9]
    team1_q3_pts = team1_linescores[10]
    team1_q4_pts = team1_linescores[11]
    team1_total_pts = team1_linescores[22]

    team2_q1_pts = team2_linescores[8]
    team2_q2_pts = team2_linescores[9]
    team2_q3_pts = team2_linescores[10]
    team2_q4_pts = team2_linescores[11]
    team2_total_pts = team2_linescores[22]
    # ct1.write(team1_total_pts)
    # ct2.write(team2_total_pts)


    h1, h2, h3 = st.columns((1,1,1))

    h1.write(f"  ##### Quarter: {quarter} - Time: {time}")
    h2.write(f" ###### Location: {arena} - TV: {homeBroadcast} & {awayBroadcast}")
    h3.button("Refresh")
    ct1, ct2 = st.columns((1,1))
    ct11, ct22 = st.columns((1,1))
    ct111, ct222 = st.columns((1,1))
    ct1.write(f"## {team1} - {team1_total_pts}")
    
    ct11.write(f"#### Q1: {team1_q1_pts} Q2: {team1_q2_pts} Q3: {team1_q3_pts} Q4: {team1_q4_pts}")
    with ct111:
        for i in range(len(team1_starters_condensed)):
            player = team1_starters_condensed.values[i][0]
            playerid = team1_starters_condensed.values[i][2]
            pos = team1_starters_condensed.values[i][1]
            comment = team1_starters_condensed.values[i][3]
            if "DNP" not in comment:
                if pos != "":
                    st.write(f"#### {pos} - {player}")
                else:
                    st.write(f"#### {player}")
                
                if pos != "":
                    st.image(f"{head_shot_url}{playerid}.png", width=150)
                else:
                    st.image(f"{head_shot_url}{playerid}.png", width=100)

    with ct222:
        for i in range(len(team2_starters_condensed)):
            player = team2_starters_condensed.values[i][0]
            playerid = team2_starters_condensed.values[i][2]
            pos = team2_starters_condensed.values[i][1]
            comment = team2_starters_condensed.values[i][3]
            if "DNP" not in comment:
                if pos != "":
                    st.write(f"#### {pos} - {player}")
                else:
                    st.write(f"#### {player}")
            
                if pos != "":
                    st.image(f"{head_shot_url}{playerid}.png", width=150)
                else:
                    st.image(f"{head_shot_url}{playerid}.png", width=100)

    ct2.write(f"## {team2} - {team2_total_pts}")
    ct22.write(f"#### Q1: {team2_q1_pts} Q2: {team2_q2_pts} Q3: {team2_q3_pts} Q4: {team2_q4_pts}")
    # ct2.write(team2_starters_condensed)



    st.write(game_log.get_data_frames()[0])
    st.write(scoreBoard.get_dict())        
    st.write(players_stats)
    st.write(linescores)

    st.write(bx.get_dict())