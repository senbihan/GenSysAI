import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from gensysai.designer import SystemDesigner


st.title("GenSys AI")
st.subheader("A GPT-Driven Automated Distributed System Designer")
DEFAULT_MESSAGE = 'Design a system that ...'

open_ai_key = st.text_input("Enter OpenAI API Key", type="password")
if open_ai_key:
    os.environ["OPENAI_API_KEY"] = open_ai_key
    llm = ChatOpenAI(temperature=0.1, max_tokens= 512, model_name='gpt-3.5-turbo')

    form = st.form(key='my_form')
    problem_statement = form.text_input("Enter the problem statement: ", DEFAULT_MESSAGE)
    cloud_option = form.selectbox('Cloud Provider',
    ('Azure', 'AWS', 'GCP', 'Any'))
    submit = form.form_submit_button(label='Generate')
    
    if submit and problem_statement != '' and problem_statement != DEFAULT_MESSAGE:
        designer = SystemDesigner(llm=llm, cloud_provider=cloud_option, verbose=False)
        st.text("Please have patience while we generate the design as per your requirement...")

        designer.design(problem_statement=problem_statement)
        st.markdown(designer.generate_markdown())