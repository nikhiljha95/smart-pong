import streamlit as st
import pandas as pd
from utils import *

def correct_match():
    with st.form("correct_match_form"):
        
        ucolmid, ucol1, ucol2 = st.columns([.1, .45, .45])
        with ucolmid:
            mid = st.text_input("Match")
        with ucol1:
            p1 = st.text_input("Winner")
        with ucol2:
            p2 = st.text_input("Loser")
        ucols1, ucols2, ucols3, ucols4, ucols5 = st.columns(5)
        with ucols1:
            s1 = st.text_input("Set 1 score")
        with ucols2:
            s2 = st.text_input("Set 2 score")
        with ucols3:
            s3 = st.text_input("Set 3 score")
        with ucols4:
            s4 = st.text_input("Set 4 score")
        with ucols5:
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
            _ = add_or_update_match(result, int(mid))
            elo_from_scratch()
            st.success(f"Match {mid} updated!")
            st.rerun()


def correct_match_doubles():
    with st.form("correct_match_form"):
        
        ucolmid, ucol11, ucol12, ucol21, ucol22 = st.columns([.1, .225, .225, .225, .225])
        ucols1, ucols2, ucols3, ucols4, ucols5 = st.columns(5)
        
        with ucolmid:
            mid = st.text_input("Match")
        with ucol11:
            p11 = st.text_input("Winner 1")
        with ucol12:
            p12 = st.text_input("Winner 2")
        with ucol21:
            p21 = st.text_input("Loser 1")
        with ucol22:
            p22 = st.text_input("Loser 2")
        with ucols1:
            s1 = st.text_input("Set 1 score")
        with ucols2:
            s2 = st.text_input("Set 2 score")
        with ucols3:
            s3 = st.text_input("Set 3 score")
        with ucols4:
            s4 = st.text_input("Set 4 score")
        with ucols5:
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
            _ = add_or_update_match(result, mid_update=int(mid), singles=False)
            elo_from_scratch(singles=False)
            st.success(f"Match {mid} updated!")
            st.rerun()