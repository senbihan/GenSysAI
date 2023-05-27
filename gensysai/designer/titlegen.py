from .openaioperation import *
from langchain.llms import BaseLLM
from langchain import PromptTemplate, LLMChain
from ..prompts import Prompts


class TitleGenerator(OpenAIOperation):
    '''Generates a title of the system under design'''

    def __init__(self, 
            llm:BaseLLM,
            verbose:bool):

        self.llm = llm
        prompt = PromptTemplate(template=  Prompts.TitleGenerationPrompt,
                                input_variables=['input'])
        self.__llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=verbose)

    def generate_title(self, problem_statement):
        return self.__llm_chain.run(input=problem_statement)
    
    def get_request_count(self):
        return 1