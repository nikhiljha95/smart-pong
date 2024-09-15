import streamlit as st
from utils import *

def show_elo(singles=True):
    st.dataframe(display_elo(singles), hide_index=True)
    st.pyplot(plot_elo(singles))