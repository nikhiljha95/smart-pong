import streamlit as st
from utils import *
from section_new_match import *
from section_elo import *
from section_update_matches import *



#############################################
############### VISUALISATION ###############
#############################################

st.title("SmartPong")

st.write("## New match")
insert_new_match()

st.write("## ELO ranking")
show_elo()

st.write('## Delete or update match')
update_or_delete_match()


st.write("## Last 20 matches")
st.dataframe(display_matches(), hide_index=True)