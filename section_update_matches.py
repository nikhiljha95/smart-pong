import streamlit as st
import pandas as pd
from utils import *

    
def update_or_delete_match():
    mid = st.number_input("Enter MatchID to update or delete", value=load_matches().MatchID.max(), step=1, min_value=1)

    matches = load_matches()

    try:
        m = matches[matches.MatchID==int(mid)]
    except KeyError:
        st.write("No match with such ID")
    st.dataframe(m, hide_index=True)

    col1, col2 = st.columns(2)
        
    # If user chooses to delete the row
    with col1:
        if st.button("Delete"):
            delete_and_reorder_matches(mid)
            elo_from_scratch()

    # If user chooses to update the row
    with col2:
        pass
        #if st.button("Update"):
        #    u_result = st.text_input("Updated result")
        #    submit_update = st.button("Submit")
        #    if submit_update:
        #        add_match(u_result, match_id_update=mid, match_date_update=m.Date)
        #        elo_from_scratch()