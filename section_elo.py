import streamlit as st
from utils import *

def show_elo():
    st.dataframe(display_elo(), hide_index=True)
    st.pyplot(plot_elo())