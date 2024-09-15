import streamlit as st
from utils import *


def insert_new_match():
    with st.form("match_form"):
        col1, col2 = st.columns(2)
        with col1:
            p1 = st.text_input("Winner")
        with col2:
            p2 = st.text_input("Loser")
        cols1, cols2, cols3, cols4, cols5 = st.columns(5)
        with cols1:
            s1 = st.text_input("Set 1 score")
        with cols2:
            s2 = st.text_input("Set 2 score")
        with cols3:
            s3 = st.text_input("Set 3 score")
        with cols4:
            s4 = st.text_input("Set 4 score")
        with cols5:
            s5 = st.text_input("Set 5 score")
            
        submit = st.form_submit_button("Submit")

        if submit:
            result = {
                'p1': p1,
                'p2': p2,
                's1': s1,
                's2': s2,
                's3': s3,
                's4': s4,
                's5': s5,
            }
            match_id = add_or_update_match(result)
            elo1_new, elo2_new, delta1, delta2 = update_elo(match_id, [p1, p2])
            st.success(f"Match {match_id} added")
            st.write(f"New ELO for {p1}: {elo1_new:.2f} ({delta1:+.2f})")
            st.write(f"New ELO for {p2}: {elo2_new:.2f} ({delta2:+.2f})")

def insert_new_match_doubles():
    with st.form("match_form"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            p11 = st.text_input("Winner 1")
        with col2:
            p12 = st.text_input("Winner 2")
        with col3:
            p21 = st.text_input("Loser 1")
        with col4:
            p22 = st.text_input("Loser 2")

        cols1, cols2, cols3, cols4, cols5 = st.columns(5)
        with cols1:
            s1 = st.text_input("Set 1 score")
        with cols2:
            s2 = st.text_input("Set 2 score")
        with cols3:
            s3 = st.text_input("Set 3 score")
        with cols4:
            s4 = st.text_input("Set 4 score")
        with cols5:
            s5 = st.text_input("Set 5 score")
            
        submit = st.form_submit_button("Submit")

        if submit:
            result = {
                'p11': p11,
                'p12': p12,
                'p21': p21,
                'p22': p22,
                's1': s1,
                's2': s2,
                's3': s3,
                's4': s4,
                's5': s5,
            }
            match_id = add_or_update_match(result, singles=False)
            players=[p11, p12, p21, p22]
            elos_new, delta1, delta2 = update_elo(match_id, players, singles=False)
            st.success(f"Match {match_id} added")
            st.write(f"New ELO for {p11}: {elos_new[0]:.2f} ({delta1:+.2f})")
            st.write(f"New ELO for {p12}: {elos_new[1]:.2f} ({delta1:+.2f})")
            st.write(f"New ELO for {p21}: {elos_new[2]:.2f} ({delta2:+.2f})")
            st.write(f"New ELO for {p22}: {elos_new[3]:.2f} ({delta2:+.2f})")