import streamlit as st
from utils import *
from section_new_match import *
from section_elo import *
from section_correct_matches import *

st.title("SmartPong - doubles")

st.write("## New match")
insert_new_match_doubles()

st.write("## ELO ranking")
show_elo(singles=False)

st.write("## Last 20 matches")
st.dataframe(display_matches(singles=False), hide_index=True)


st.write('## Correct match')
correct_match_doubles()