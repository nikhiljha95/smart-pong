import streamlit as st
from utils import *
from section_new_match import *
from section_elo import *
from section_correct_matches import *

st.set_page_config(page_title="SmartPong - singles 🏓", page_icon="🏓")
st.title("SmartPong - singles 🏓")



st.write("## New match")
insert_new_match()

st.write("## ELO ranking")
show_elo()

st.write("## Last 20 matches")
st.dataframe(display_matches(), hide_index=True)


st.write('## Correct match')
correct_match()