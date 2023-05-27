from .openaioperation import OpenAIOperation
from .base import BaseComponentDesigner
from langchain.llms import BaseLLM
from ..models import Component, ServiceComponent
from langchain import PromptTemplate, LLMChain
from ..prompts import Prompts
from typing import Dict
from langchain.output_parsers import PydanticOutputParser

class ServiceComponentDesigner(BaseComponentDesigner, OpenAIOperation):
    '''Designs a Service component based on the provided component details'''

    def __init__(self,
            llm : BaseLLM,
            verbose : bool = False
            ) -> None:
        
        self.__parser = PydanticOutputParser(pydantic_object=ServiceComponent)
        prompt = PromptTemplate(template=  Prompts.ServiceComponentDesignerPrompt,
                                input_variables=['component'],
                                partial_variables={"format_instructions": self.__parser.get_format_instructions()})
        self.__llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=verbose)

    
    def design(self,
               component : Component,
               cloud_provider : str = 'Any',
               additional_input : Dict[str,str] = None):

        if component.component_type != 'Service':
            raise ValueError("This Designer is suitable for Service Components only")
        
        output = self.__llm_chain.run(component = str(component))
        return self.__parser.parse(output)
    
    def get_request_count(self):
        return 1