import streamlit as st

from app_openai import simple_chat, simple_summary

from langchain_community.document_loaders import NewsURLLoader


language = st.selectbox('add a language', ['German', 'Persian', 'English', 'French'])

prompt = st.text_input('enter your prompt')

if st.button('Ask ChatGPT'):
    result = simple_chat(prompt, language)
    st.write(result)

url = st.text_input('enter your url',  value="https://medium.com/enrique-dans/the-time-has-come-to-ban-robocalls-using-ai-generated-voices-d4b0ea3d665e")

if st.button('Get News'):
    urls = [
        url,
    ]
    loader = NewsURLLoader(urls=urls)
    data = loader.load()
    st.header("Content")
    st.write(data[0].page_content)
    st.header("Summary")
    st.write(simple_summary(language, data[0].page_content))
