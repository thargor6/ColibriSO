from langchain_community.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name='gpt-4')


def simple_chat(prompt, language):
  code_prompt = PromptTemplate(
    template="Write a short " + prompt + ", in {language}",
    input_variables=["language"]
  )
  code_chain = LLMChain(
     llm=llm, prompt=code_prompt)
  result = code_chain({"language": language})
  return result["text"]

def simple_summary(language, text):
  code_prompt = PromptTemplate(
    template="Write a short summary of the following text in {language}:\n {text}",
    input_variables=["language", "text"]
  )
  code_chain = LLMChain(
    llm=llm, prompt=code_prompt)
  result = code_chain({"language": language, "text": text})
  print(result)

  return result["text"]
