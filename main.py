import os
from getpass import getpass
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from gensysai.designer import SystemDesigner


if __name__ == '__main__':
    OPENAI_API_KEY = getpass("Enter your OPEN AI API key: ")
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

    ## TODO: parameterize model names
    llm = ChatOpenAI(temperature=0.1, max_tokens= 512, model_name='gpt-3.5-turbo')
    designer = SystemDesigner(llm=llm, verbose=True)

    problem_statement = input("Enter the problem statement: ")
    designer.design(problem_statement=problem_statement)
    designer.dump_to_md_file("./samples/generated/design001.md")
