import streamlit as st
import pandas as pd
from datetime import datetime
import math
import json
import matplotlib.pyplot as plt
import numpy as np

# File to store player ELOs
elo_file = "files/elo_rankings.json"
elo_doubles_file = "files/elo_rankings_doubles.json"
# File to store the matches
matches_file = "files/matches.csv"
matches_doubles_file = "files/matches_doubles.csv"

def add_or_update_match(result, mid_update=-1, singles=True):


    if mid_update > 0:
        if singles:
            df = pd.read_csv(matches_file)
        else:
            df = pd.read_csv(matches_doubles_file)
        match_id = str(mid_update)

    else:
        # Check if file exists, otherwise create it
        try:
            if singles:
                df = pd.read_csv(matches_file)
            else:
                df = pd.read_csv(matches_doubles_file)
            match_id = df["MatchID"].max() + 1
        except FileNotFoundError:
            if singles:
                df = pd.DataFrame(
                    columns=["MatchID", "Date","Player1", "Player2", 
                            "Set1", "Set2", "Set3", "Set4", "Set5"])
            else:
                df = pd.DataFrame(
                    columns=["MatchID", "Date",
                             "Winner1", "Winner2",
                             "Loser1", "Loser2",
                            "Set1", "Set2", "Set3", "Set4", "Set5"])
                
            df.MatchID.astype(np.int64)
            df.Date.astype(str)
            match_id = 1
    
    if singles:
        player1, player2 = result['p1'], result['p2']
    else:
        player11, player12, player21, player22 = result['p11'], result['p12'],result['p21'], result['p22']
    sets = [result[f's{x}'] for x in range(1,6)]
    
    if mid_update > 0:
        
        if singles:
            df.loc[df.MatchID==np.int64(mid_update), "Player1"] = player1
            df.loc[df.MatchID==np.int64(mid_update), "Player2"] = player2
            df.loc[df.MatchID==np.int64(mid_update), "Set1"] = sets[0]
            df.loc[df.MatchID==np.int64(mid_update), "Set2"] = sets[1]
            df.loc[df.MatchID==np.int64(mid_update), "Set3"] = sets[2]
            df.loc[df.MatchID==np.int64(mid_update), "Set4"] = sets[3]
            df.loc[df.MatchID==np.int64(mid_update), "Set5"] = sets[4]
        else:
            df.loc[df.MatchID==np.int64(mid_update), "Winner1"] = player11
            df.loc[df.MatchID==np.int64(mid_update), "Winner2"] = player12
            df.loc[df.MatchID==np.int64(mid_update), "Loser1"] = player21
            df.loc[df.MatchID==np.int64(mid_update), "Loser2"] = player22
            df.loc[df.MatchID==np.int64(mid_update), "Set1"] = sets[0]
            df.loc[df.MatchID==np.int64(mid_update), "Set2"] = sets[1]
            df.loc[df.MatchID==np.int64(mid_update), "Set3"] = sets[2]
            df.loc[df.MatchID==np.int64(mid_update), "Set4"] = sets[3]
            df.loc[df.MatchID==np.int64(mid_update), "Set5"] = sets[4]

    else:
        date = str(datetime.today().strftime('%Y-%m-%d'))
        if singles:
            new_match = pd.DataFrame([[match_id, date, player1, player2, *sets]], 
                                    columns=["MatchID", "Date", "Player1", "Player2", "Set1", "Set2", "Set3", "Set4", "Set5"])
        else:
            new_match = pd.DataFrame(
                [[match_id, date, player11, player12, player21, player22, *sets]],
                columns=[
                    "MatchID", "Date",
                    "Winner1", "Winner2",
                    "Loser1", "Loser2",
                    "Set1", "Set2", "Set3", "Set4", "Set5"])
    
        df = pd.concat([df, new_match], ignore_index=True)
    
    if singles:
        df.to_csv(matches_file, index=False)
    else:
        df.to_csv(matches_doubles_file, index=False)

    return match_id

def load_matches(singles=True):
    if singles:
        return pd.read_csv(matches_file)
    else:
        return pd.read_csv(matches_doubles_file)
# Initialize or load existing ELO data
def load_elo(singles=True):
    try:
        if singles:
            elo = json.loads(open(elo_file, 'r').read())
        else:
            elo = json.loads(open(elo_doubles_file, 'r').read())
    except FileNotFoundError:
        elo = {}
    return elo


# Update ELO based on match results
def update_elo(match_id, players, singles=True):
    K = 32  # ELO constant

    elo = load_elo(singles)

    for p in players:
        if p not in elo:
            elo[p] = [(-1, 500.)]
    
    elos = []
    for p in players:
        elos.append(elo[p][-1][1])
    
    # Calculate expected score

    if singles:
        elo1 = elos[0]
        elo2 = elos[1]
    else:
        elo1 = np.mean([elos[0], elos[1]])
        elo2 = np.mean([elos[2], elos[3]])

    expected1 = 1 / (1 + math.pow(10, (elo2 - elo1) / 400))
    expected2 = 1 / (1 + math.pow(10, (elo1 - elo2) / 400))
    
    # Actual score (1 for winner, 0 for loser)
    actual1 = 1 
    actual2 = 0
    
    # Calculate delta
    delta1 = K * (actual1 - expected1)
    delta2 = K * (actual2 - expected2)

    # Update ELO
    if singles:
        elo1_new = elos[0] + delta1
        elo2_new = elos[1] + delta2
        elos_new = [elo1_new, elo2_new]
        elo[players[0]].append((int(match_id), elo1_new))
        elo[players[1]].append((int(match_id), elo2_new))
    else:
        elo11_new = elos[0] + delta1
        elo12_new = elos[1] + delta1
        elo21_new = elos[2] + delta2
        elo22_new = elos[3] + delta2
        elos_new = [elo11_new, elo12_new,elo21_new, elo22_new]
        print(elos_new)
        elo[players[0]].append((int(match_id), elo11_new))
        elo[players[1]].append((int(match_id), elo12_new))
        elo[players[2]].append((int(match_id), elo21_new))
        elo[players[3]].append((int(match_id), elo22_new))

    if singles:
        f = open(elo_file, 'w')
    else:
        f = open(elo_doubles_file, 'w')
    f.write(json.dumps(elo))
    f.close()

    if singles:
        st.session_state['p1'] = players[0]
        st.session_state['p2'] = players[1]
    else:
        st.session_state['p1'] = players[0]
        st.session_state['p2'] = players[1]
        st.session_state['p3'] = players[2]
        st.session_state['p4'] = players[3]
        
    st.session_state['d1'] = delta1
    st.session_state['d2'] = delta2

    return elos_new, delta1, delta2

def display_elo(singles=True):

    # Load ELO from file and format it correctly

    elo_json = load_elo(singles)
    elo_data = [(0, k, v[-1][1]) for k,v in elo_json.items()]
    elo_df = pd.DataFrame(elo_data,columns=["Position", "Name", "ELO"])
    elo_df = elo_df.sort_values(by="ELO", ascending=False)
    elo_df.Position = range(1, len(elo_df)+1)


    # If a result has been inserted or update,
    # show update in table
    if "p1" in st.session_state:

        player1 = st.session_state['p1']
        player2 = st.session_state['p2']

        if not singles:
            player3 = st.session_state['p3']
            player4 = st.session_state['p4']
        
        delta1 = st.session_state['d1']
        delta2 = st.session_state['d2']

        # Calculate the previous ELO

        players = [player1, player2]
        if not singles:
            players.extend([player3, player4])

        old_elo = elo_df.copy(deep=True)

        if singles:
            old_elo.loc[old_elo.Name==player1, "ELO"] = old_elo.loc[old_elo.Name==player1, "ELO"].values[0] - delta1
            old_elo.loc[old_elo.Name==player2, "ELO"] = old_elo.loc[old_elo.Name==player2, "ELO"].values[0] - delta2
        else:

            print(old_elo)

            old_elo.loc[old_elo.Name==player1, "ELO"] = old_elo.loc[old_elo.Name==player1, "ELO"].values[0] - delta1
            old_elo.loc[old_elo.Name==player2, "ELO"] = old_elo.loc[old_elo.Name==player2, "ELO"].values[0] - delta1
            old_elo.loc[old_elo.Name==player3, "ELO"] = old_elo.loc[old_elo.Name==player3, "ELO"].values[0] - delta2
            old_elo.loc[old_elo.Name==player4, "ELO"] = old_elo.loc[old_elo.Name==player4, "ELO"].values[0] - delta2

        old_elo = old_elo.sort_values(by="ELO", ascending=False)
        old_elo.Position = range(1, len(old_elo)+1)
        
        # Calculate differences between previous and current ELO

        new_rank = list(elo_df.Name.values)
        old_rank = list(old_elo.Name.values)
        idx_change=[old_rank.index(x)-i for i, x in enumerate(new_rank)]

        # Format updated values

        if singles:
            elo_df.loc[elo_df.Name==player1, "ELO"] = f"{elo_df.loc[elo_df.Name==player1, 'ELO'].values[0]:.2f} ({delta1:+.2f})"
            elo_df.loc[elo_df.Name==player2, "ELO"] = f"{elo_df.loc[elo_df.Name==player2, 'ELO'].values[0]:.2f} ({delta2:+.2f})"

        else:
            elo_df.loc[elo_df.Name==player1, "ELO"] = f"{elo_df.loc[elo_df.Name==player1, 'ELO'].values[0]:.2f} ({delta1:+.2f})"
            elo_df.loc[elo_df.Name==player2, "ELO"] = f"{elo_df.loc[elo_df.Name==player2, 'ELO'].values[0]:.2f} ({delta1:+.2f})"
            elo_df.loc[elo_df.Name==player3, "ELO"] = f"{elo_df.loc[elo_df.Name==player3, 'ELO'].values[0]:.2f} ({delta2:+.2f})"
            elo_df.loc[elo_df.Name==player4, "ELO"] = f"{elo_df.loc[elo_df.Name==player4, 'ELO'].values[0]:.2f} ({delta2:+.2f})"

        elo_df.loc[~elo_df.Name.isin(players), "ELO"] = elo_df.loc[~elo_df.Name.isin(players), "ELO"].apply(lambda x: f"{x:.2f}")
        
        for n,v in zip(new_rank, idx_change):
            if v != 0:
                elo_df.loc[elo_df.Name==n, "Position"] = f"{elo_df.loc[elo_df.Name==n, 'Position'].values[0]} ({v:+d})"

    else:
        elo_df.ELO = elo_df.ELO.apply(lambda x: f"{x:.2f}")

    return elo_df

def plot_elo(singles=True):
    fig, ax = plt.subplots()
    elo_json = load_elo(singles)
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

def display_matches(singles=True):
    try:
        if singles:
            df = pd.read_csv(matches_file)
        else:
            df = pd.read_csv(matches_doubles_file)
    except FileNotFoundError:
        if singles:
            df = pd.DataFrame(columns=["MatchID", "Date","Player1", "Player2", 
                                        "Set1", "Set2", "Set3", "Set4", "Set5"])
        else:
            df = pd.DataFrame(columns=[
                "MatchID", "Date",
                "Winner1", "Winner2",
                "Loser1", "Loser2",
                "Set1", "Set2", "Set3", "Set4", "Set5"])

    return df.tail(20)

def elo_from_scratch(singles=True):
    matches = load_matches(singles)
    
    if singles:
        f = open(elo_file, 'w')
    else:
        f = open(elo_doubles_file, 'w')
        f.write(json.dumps({}))
        f.close()

    if singles:
        for mid, p1, p2 in zip(
            matches.MatchID.values,
            matches.Player1.values,
            matches.Player2.values,
        ):
            _,_,_ = update_elo(mid, [p1,p2])
    else:
        for mid, p11, p12, p21, p22 in zip(
            matches.MatchID.values,
            matches.Winner1.values,
            matches.Winner2.values,
            matches.Loser1.values,
            matches.Loser2.values,
        ):
            _,_,_ = update_elo(mid, [p11,p12, p21, p22], singles)