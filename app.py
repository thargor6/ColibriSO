import streamlit as st

from app_database import connect_to_colibri_db
from app_openai import simple_chat, simple_summary

from langchain_community.document_loaders import NewsURLLoader

from app_sqlite import create_project, create_task, create_snippet, create_snippet_part

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

    conn = connect_to_colibri_db()
    snippet = ('URL Content ', '2015-01-01');
    snippet_id = create_snippet(conn, snippet)
    snippet_part_url = (snippet_id, 'URL', 'en', url);
    create_snippet_part(conn, snippet_part_url)

    st.header("Content")
    snippet_part_content = (snippet_id, 'content', 'en', data[0].page_content);
    create_snippet_part(conn, snippet_part_content)
    st.write(data[0].page_content)

    st.header("Summary")
    summary = simple_summary(language, data[0].page_content)
    snippet_part_summary = (snippet_id, 'summary', language, summary);
    create_snippet_part(conn, snippet_part_summary)
    st.write(summary)


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
