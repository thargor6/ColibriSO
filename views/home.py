import streamlit as st

from app_openai import simple_chat
import app_constants as const

def load_view():
    st.title('Home Page')
    language = st.selectbox('add a language', [const.LANGUAGE_DE, const.LANGUAGE_FA, const.LANGUAGE_EN, const.LANGUAGE_FR])

    prompt = st.text_input('enter your prompt')

    if st.button('Ask ChatGPT'):
      result = simple_chat(prompt, language)
      st.write(result)