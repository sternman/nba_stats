import streamlit as st
import pandas as pd
import requests
import nba_api
from datetime import datetime, timedelta

from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
# from nba_api.stats.static import players

from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2
from nba_api.stats.endpoints.boxscorescoringv2 import BoxScoreScoringV2
from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
from nba_api.stats.endpoints import PlayByPlayV2
from nba_api.stats.endpoints.videoevents import VideoEvents

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
    st.session_state.scoreboard = scoreBoard.get_available_data()

if "scoreboard" in st.session_state:
    scoreBoard = ScoreboardV2(game_date=dt_start, league_id=leagues[0], timeout=30)
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

    bx = BoxScoreScoringV2(game_id=lookup_gameid, timeout=20 )
    bxs = BoxScoreSummaryV2(game_id=lookup_gameid, timeout=20 )
    play_by_play_v2 = PlayByPlayV2(game_id=lookup_gameid, timeout=20)
    df_play_by_play_v2 = play_by_play_v2.get_data_frames()[0]
    
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
    team1_ot_pts = team1_linescores[12]
    team1_total_pts = team1_linescores[22]

    team2_q1_pts = team2_linescores[8]
    team2_q2_pts = team2_linescores[9]
    team2_q3_pts = team2_linescores[10]
    team2_q4_pts = team2_linescores[11]
    team2_ot_pts = team2_linescores[12]
    team2_total_pts = team2_linescores[22]
    # ct1.write(team1_total_pts)
    # ct2.write(team2_total_pts)


    h1, h2, h3 = st.columns((1,1,1))

    h1.write(f"  ##### Quarter: {quarter} - Time: {time}")
    h2.write(f" ###### Location: {arena} - TV: {homeBroadcast} & {awayBroadcast}")
    if h3.button("↩️"):
        st.rerun()
    ct1, ct2 = st.columns((1,1))
    ct11, ct22 = st.columns((1,1))
    ct111, ct222 = st.columns((1,1))
    ct1.write(f"## {team1} - {team1_total_pts}")
    
    ot1 = ""
    if team1_ot_pts > 0:
        ot1 = f" OT: {team1_ot_pts}"
    ct11.write(f"##### Q1: {team1_q1_pts} Q2: {team1_q2_pts} Q3: {team1_q3_pts} Q4: {team1_q4_pts}{ot1}")
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
                    st.image(f"{head_shot_url}{playerid}.png", width=125)

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
                    st.image(f"{head_shot_url}{playerid}.png", width=125)

    ct2.write(f"## {team2} - {team2_total_pts}")
    ot2 = ""
    if team2_ot_pts > 0:
        ot2 = f" OT: {team2_ot_pts}"
    ct22.write(f"##### Q1: {team2_q1_pts} Q2: {team2_q2_pts} Q3: {team2_q3_pts} Q4: {team2_q4_pts}{ot2}")
    # ct2.write(team2_starters_condensed)
    # st.write(df_play_by_play_v2)
    df_play_by_play_v2 = df_play_by_play_v2[["EVENTNUM", "PERIOD", "PCTIMESTRING", "SCORE", "HOMEDESCRIPTION", "VISITORDESCRIPTION", "PLAYER1_NAME", "PLAYER2_NAME", "PLAYER3_NAME", "VIDEO_AVAILABLE_FLAG"]]
    df_play_by_play_v2 = df_play_by_play_v2.rename(columns={"PCTIMESTRING":"CLOCK"})
    df_play_by_play_v2 = df_play_by_play_v2.fillna("")
    
    df_play_by_play_v2["DESCRIPTION"] = df_play_by_play_v2["HOMEDESCRIPTION"] + df_play_by_play_v2["VISITORDESCRIPTION"] #+ df_play_by_play_v2[""]
    df_play_by_play_v2 = df_play_by_play_v2[["EVENTNUM", "PERIOD", "CLOCK", "SCORE", "DESCRIPTION", "PLAYER1_NAME", "PLAYER2_NAME", "PLAYER3_NAME", "VIDEO_AVAILABLE_FLAG"]]
    df_play_by_play_v2 = df_play_by_play_v2.sort_values(by="EVENTNUM", ascending=False)
    def highlight_score(s):
        if s["SCORE"] != "":
            return ['background-color: lightgreen']*len(s)
        if "FOUL" in s["DESCRIPTION"]:
            return ['background-color: pink']*len(s)
        if "SUB" in s["DESCRIPTION"]:
            return ['background-color: lightblue']*len(s)
        if "Timeout" in s["DESCRIPTION"]:
            return ['background-color: lightyellow']*len(s)
        return ['background-color: white']*len(s)
        # return ['background-color: lightgreen']*len(s) if s["SCORE"] != "" else ['background-color: white']*len(s)
    
    df_play_by_play_v2 = df_play_by_play_v2[["EVENTNUM", "PERIOD", "CLOCK", "SCORE", "DESCRIPTION", "PLAYER1_NAME", "PLAYER2_NAME", "PLAYER3_NAME"]]
    df_play_by_play_v2 = df_play_by_play_v2.head(20)
    df_play_by_play_v2 = df_play_by_play_v2.style.apply(highlight_score, axis=1)

    # df_play_by_play_v2 = df_play_by_play_v2.style.set_properties(**{'text-align': 'center'})
    st.table(df_play_by_play_v2)#, selection_mode="single-row", on_select="rerun")
    # st.write(selected_row)
    # if len(selected_row["selection"]["rows"]) > 0:
    #     # st.write(selected_row)
    #     row = df_play_by_play_v2.iloc[selected_row["selection"]["rows"][0]]
    #     eventnum = row["EVENTNUM"]
    #     is_video_available = row["VIDEO_AVAILABLE_FLAG"]
    #     ve = VideoEvents(game_id=lookup_gameid, game_event_id=eventnum)
    #     ve_data = ve.get_dict()
    #     uuid = ve_data["resultSets"]["Meta"]["videoUrls"][0]["uuid"]
    #     # st.write(f"http://stats.nba.com/stats/videoevents/?gameId={lookup_gameid}&gameEventId={eventnum}")
    #     vid_url = f"http://stats.nba.com/stats/videoevents/?gameId={lookup_gameid}&gameEventId={eventnum}"
    #     # st.write(eventnum)
    #     st.write("row")
    #     if is_video_available:
    #         pass
            # st.video(vid_url)


    # st.write(lookup_gameid)
    
    
    
    # st.write(ve_data)
    # uuid = ve_data["resultSets"]["Meta"]["videoUrls"][0]["uuid"]
    # st.write(f"http://stats.nba.com/stats/videoevents/?gameId={lookup_gameid}&gameEventId={event_id}")
    # vid_url = f"http://stats.nba.com/stats/videoevents/?gameId={lookup_gameid}&gameEventId={event_id}"
    # st.video(vid_url)
    # res = requests.get(vid_url)
    # st.write(vid_url)
    # st.write(game_log.get_data_frames()[0])
    # st.write(scoreBoard.get_dict())        
    # st.write(players_stats)
    # st.write(linescores)

    # st.write(bx.get_dict())