# MIT License
#
# ColibriSO - a tool for organizing information of all kinds, written in Python and Streamlit.
# Copyright (C) 2022-2024 Andreas Maschke
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import streamlit as st
#from langchain_community.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import backend.constants as const




def simple_chat(prompt, language):
  llm = ChatOpenAI(temperature=const.OPENAI_DFLT_TEMPERATURE, model_name=const.OPENAI_DFLT_MODEL, api_key=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else None)
  code_prompt = PromptTemplate(
    template="Write a short " + prompt + ", in {language}. After that, repeat the same in English",
    input_variables=["language"]
  )
  code_chain = LLMChain(
     llm=llm, prompt=code_prompt)
  result = code_chain({"language": language})
  return result["text"]

def simple_summary(language, text, brief=True):
  llm = ChatOpenAI(temperature=const.OPENAI_DFLT_TEMPERATURE, model_name=const.OPENAI_DFLT_MODEL, api_key=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else None)
  code_prompt = PromptTemplate(
    template="Write a {summary_type} summary of the following text in {language} language:\n {text}",
    input_variables=["summary_type", "language", "text"]
  )
  code_chain = LLMChain(
    llm=llm, prompt=code_prompt)
  result = code_chain({"summary_type": "brief" if brief is True else "comprehensive", "language": language, "text": text})
  return result["text"]


def simple_explanation(prompt, language, ref_language, explanation_type):
  llm = ChatOpenAI(temperature=const.OPENAI_DFLT_TEMPERATURE, model_name=const.OPENAI_DFLT_MODEL, api_key=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else None)
  conv_explanation_type = "brief" if explanation_type == const.PART_EXPLANATION_BRIEF else "comprehensive"

  template="In {language} language, write a truly {explanation_type} explanation of the term \"{prompt}\" ."
  if ref_language is not None and ref_language != language:
    template += "Repeat the same in {ref_language} language."

  code_prompt = PromptTemplate(
    template=template,
    input_variables=["prompt", "explanation_type", "language", "ref_language"]
  )
  code_chain = LLMChain(
    llm=llm, prompt=code_prompt)
  result = code_chain({"prompt": prompt, "language": language, "ref_language": ref_language, "explanation_type": conv_explanation_type})
  return result["text"]

def simple_translate(input_text, language):
  llm = ChatOpenAI(temperature=const.OPENAI_DFLT_TEMPERATURE, model_name=const.OPENAI_DFLT_MODEL, api_key=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else None)

  template=f"Translate the following text into {language} language:\n\n {input_text}"

  code_prompt = PromptTemplate(
    template=template,
    input_variables=["input_text", "language"]
  )
  code_chain = LLMChain(
    llm=llm, prompt=code_prompt)
  result = code_chain({"input_text": input_text, "language": language})
  return result["text"]


from pathlib import Path
from openai import OpenAI

def text_to_speech(text, voice=const.OPENAI_DFLT_SPEECH_VOICE, model=const.OPENAI_DFLT_SPEECH_MODEL):
  client = OpenAI(api_key=st.session_state[const.SESSION_USER_OPEN_AI_API_KEY] if const.SESSION_USER_OPEN_AI_API_KEY in st.session_state else None)
  speech_file_path = Path(__file__).parent / "speech.mp3"

  response = client.audio.speech.create(
    model=model,
    voice=voice,
    input=text,
    response_format="mp3",
  )
  response.stream_to_file(speech_file_path)
  return speech_file_path
