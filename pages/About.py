import streamlit as st


# --- GENERAL SETTINGS ---
PRODUCT_NAME = "GenSys AI"
PRODUCT_TAGLINE = "A GPT-Driven Automated Distributed System Designer"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title=f"{PRODUCT_NAME} | About",
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    '''
    GenSysAI is an experimental project for helping design a distributed system. It does not provide an accurate solution yet, but it can and it will.


    ### Motivation :sunglasses:
    While designing a large-scale distributed system, an individual Software Enginner or Architect has limitations on the knowledge of not only different strategies but technologies from different cloud providers.
    Although researching about the problem, reading different blogs, books and papers give a detailed idea about them, this tool aims to provide a comprehensive gist of a distributed system that you would want to design. This can help in focused research while designing a system, 
    even can help you prepare for interviews.
    
    
    Stay tuned for next updates. :smile:
    '''
)