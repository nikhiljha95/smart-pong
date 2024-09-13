import streamlit as st
from utils import *


def insert_new_match():
    with st.form("match_form"):
        result_str = st.text_input("New match result (in the form '<Winner> <Loser> <ResultSet1> <ResultSet2> <ResultSet3> <ResultSet4> <ResultSet5>')")
        submit = st.form_submit_button("Submit")

        if submit:
            match_id, player1, player2 = add_match(result_str)
            elo1_new, elo2_new, delta1, delta2 = update_elo(match_id, player1, player2)
            st.write(f"Match {match_id} added")
            st.write(f"New ELO for {player1}: {elo1_new:.2f} ({delta1:+.2f})")
            st.write(f"New ELO for {player2}: {elo2_new:.2f} ({delta2:+.2f})")