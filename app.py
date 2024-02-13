import streamlit as st

from app_database import connect_to_colibri_db
from app_openai import simple_chat, simple_summary

from langchain_community.document_loaders import NewsURLLoader

from app_sqlite import create_connection, create_project, create_task, create_table


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


if st.button('Insert Shit'):
    conn = connect_to_colibri_db()
    with conn:
        # create a new project
        project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        project_id = create_project(conn, project)

        # tasks
        task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_task(conn, task_1)
        create_task(conn, task_2)
