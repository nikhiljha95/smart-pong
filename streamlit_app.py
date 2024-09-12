import streamlit as st
import pandas as pd
from datetime import datetime
import math
import json
import matplotlib.pyplot as plt

# File to store player ELOs
elo_file = "elo_rankings.json"
# File to store the matches
matches_file = "matches.csv"

def add_match(result_str):
    # Check if file exists, otherwise create it
    try:
        df = pd.read_csv(matches_file)
        match_id = df["MatchID"].max() + 1
    except FileNotFoundError:
        df = pd.DataFrame(columns=["MatchID", "Date","Player1", "Player2", 
                                   "Set1", "Set2", "Set3", "Set4", "Set5"])
        match_id = 1
    
    # Parse result string and create match entry
    result = result_str.split()
    date = datetime.today().strftime('%Y-%m-%d')
    player1, player2 = result[0], result[1]
    sets = result[2:]  # Remaining scores
    sets.extend([""] * (5 - len(sets)))  # Pad with empty strings if fewer than 5 sets
    
    new_match = pd.DataFrame([[match_id, date, player1, player2, *sets]], 
                             columns=["MatchID", "Date", "Player1", "Player2", "Set1", "Set2", "Set3", "Set4", "Set5"])
    
    df = pd.concat([df, new_match], ignore_index=True)
    df.to_csv(matches_file, index=False)

    return match_id, player1, player2


# Initialize or load existing ELO data
def load_elo():
    
    try:
        elo = json.loads(open(elo_file, 'r').read())
    except FileNotFoundError:
        elo = {}
    return elo


# Update ELO based on match results
def update_elo(match_id, player1, player2):
    K = 32  # ELO constant

    elo = load_elo()
    
    if player1 not in elo:
        elo[player1] = [(-1, 500.)]
    if player2 not in elo:
        elo[player2] = [(-1, 500.)]
    
    elo1 = elo[player1][-1][1]
    elo2 = elo[player2][-1][1]
    
    # Calculate expected score
    expected1 = 1 / (1 + math.pow(10, (elo2 - elo1) / 400))
    expected2 = 1 / (1 + math.pow(10, (elo1 - elo2) / 400))
    
    # Actual score (1 for winner, 0 for loser)
    actual1 = 1 
    actual2 = 0
    
    # Calculate delta
    delta1 = K * (actual1 - expected1)
    delta2 = K * (actual2 - expected2)

    # Update ELO
    elo1_new = elo1 + delta1
    elo2_new = elo2 + delta2
    
    elo[player1].append((int(match_id), elo1_new))
    elo[player2].append((int(match_id), elo2_new))

    try:
        f = open(elo_file, 'w')
    except FileNotFoundError:
        f = open(elo_file, 'w')
    f.write(json.dumps(elo))
    f.close()

    return elo1_new, elo2_new, delta1, delta2

def display_elo(player1=None, player2=None, delta1=None, delta2=None):
    
    # Create a df with position, name and ELO

    elo_json = load_elo()
    elo_data = [(0, k, v[-1][1]) for k,v in elo_json.items()]
    elo_df = pd.DataFrame(elo_data,columns=["Posizione", "Nome", "ELO"])
    elo_df = elo_df.sort_values(by="ELO", ascending=False)
    elo_df.Posizione = range(1, len(elo_df)+1)

    elo_df.ELO = elo_df.ELO.apply(lambda x: f"{x:.2f}")

    return elo_df

def plot_elo():
    fig, ax = plt.subplots()
    elo_json = load_elo()
    elo_data = [(k, v[-1][1]) for k,v in elo_json.items()]
    sorted_players = [y[0] for y in sorted(elo_data, key=lambda x:x[1], reverse=True)]
    for p in sorted_players:
        elo_trend = elo_json[p]
        elo_trend[0] = (elo_trend[1][0]-1, 500)
        ax.plot(
            [x[0] for x in elo_trend],
            [x[1] for x in elo_trend],
            label=p,
            )
        ax.legend()
    return fig

def display_matches():
    try:
        df = pd.read_csv(matches_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["MatchID", "Date","Player1", "Player2", 
                                   "Set1", "Set2", "Set3", "Set4", "Set5"])
    return df.tail(20)

#############################################
############### VISUALISATION ###############
#############################################

st.title("SmartPong")

st.write("## New match")
with st.form("match_form"):
    result_str = st.text_input("New match result (in the form '<Winner> <Loser> <ResultSet1> <ResultSet2> <ResultSet3> <ResultSet4> <ResultSet5>')")
    submit = st.form_submit_button("Submit")

    if submit:
        match_id, player1, player2 = add_match(result_str)
        elo1_new, elo2_new, delta1, delta2 = update_elo(match_id, player1, player2)
        st.write(f"Match {match_id} added")
        st.write(f"New ELO for {player1}: {elo1_new:.2f} ({delta1:+.2f})")
        st.write(f"New ELO for {player2}: {elo2_new:.2f} ({delta2:+.2f})")

        #st.table(display_elo())

st.write("## ELO ranking")
st.dataframe(display_elo(), hide_index=True)
st.pyplot(plot_elo())

st.write("## Last 20 matches")
st.dataframe(display_matches(), hide_index=True)