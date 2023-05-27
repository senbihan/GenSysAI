from .base import BaseComponentDesigner
from langchain.llms import BaseLLM
from ..models import Component
from langchain import PromptTemplate, LLMChain
from ..prompts import Prompts
from typing import Dict
from .openaioperation import OpenAIOperation

class StorageComponentDesigner(BaseComponentDesigner, OpenAIOperation):
    '''
        Designs a Storage Component based on the component details
    '''
    def __init__(self,
            llm : BaseLLM,
            verbose : bool = False
            ) -> None:
        
        prompt = PromptTemplate(template= Prompts.StorageComponentDesignerPrompt,
                                input_variables=['component', 'cloud_provider'])
        self.__llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=verbose)

    
    def design(self,
               component : Component,
               cloud_provider : str = 'Any',
               additional_input : Dict[str,str] = None):

        if component.component_type != 'Storage':
            raise ValueError("This Designer is suitable for Storage Components only")
        
        if cloud_provider not in ['AWS', 'Azure', 'GCP', 'Any']:
            raise ValueError("Cloud Provider should be from ['AWS', 'Azure', 'GCP', 'Any']")

        output = self.__llm_chain.run(component = str(component), cloud_provider=cloud_provider)
        return output
    
    def get_request_count(self):
        return 1