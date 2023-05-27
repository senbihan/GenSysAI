import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from gensysai.designer.system import SystemDesigner
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


# --- PATH SETTINGS ---
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR = THIS_DIR / "assets"
STYLES_DIR = THIS_DIR / "styles"
CSS_FILE   = STYLES_DIR / "main.css"


# --- SESSION STATE ---


# --- GENERAL SETTINGS ---
PRODUCT_NAME = "GenSys AI"
PRODUCT_TAGLINE = "A GPT-Driven Automated Distributed System Designer"


# --- PAGE CONFIG ---
st.set_page_config(
    page_title=PRODUCT_NAME,
    page_icon=":rocket:",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title(f"{PRODUCT_NAME} :rocket:")
st.subheader(f"_{PRODUCT_TAGLINE}_")
DEFAULT_MESSAGE = 'Design a system that ...'


#os.environ["OPENAI_API_KEY"] = open_ai_key
#llm = ChatOpenAI(temperature=0.1, max_tokens= 512, model_name='gpt-3.5-turbo')
llm = OpenAI(temperature=0.1, max_tokens=512, model_name='text-davinci-003')

# -- FORM --
with st.form(key='my_form'): 
    col1, col2 = st.columns([3,1])
    with col1:
        problem_statement = st.text_input("Enter the problem statement: ", DEFAULT_MESSAGE,)
        st.markdown(":bulb: `Provide a detailed problem statement for more accurate result.`_``Example: Design a system like uber where an user can book rides``_")
    with col2:
        cloud_option = st.selectbox('Preferred Cloud Provider', ('Any', 'Azure', 'AWS', 'GCP'))
    
    submit = st.form_submit_button(label='Generate')
    st.info('The generation usually takes some time, please have patience...', icon="ℹ️")


if submit and problem_statement != '' and problem_statement != DEFAULT_MESSAGE:
    
    designer = SystemDesigner(llm=llm, cloud_provider=cloud_option, verbose=False)

    try:
        designer.design(problem_statement=problem_statement)
        st.markdown(designer.generate_markdown())
    except Exception as e:
        st.error(e)

