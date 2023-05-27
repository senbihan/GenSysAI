from langchain.llms import BaseLLM
from ..models import Component
from langchain import PromptTemplate, LLMChain
from ..prompts import Prompts
from typing import Dict, List
from .base import BaseComponentDesigner
from .openaioperation import OpenAIOperation
    

class GenericComponentDesigner(BaseComponentDesigner, OpenAIOperation):
    '''Designs a Service component based on the provided component details'''

    def __init__(self,
            llm : BaseLLM,
            verbose : bool = False,
            additional_inputs : List[str] = None 
            ) -> None:
        
        self.input_variables = ['component', 'cloud_provider']
        if additional_inputs is not None:
            self.input_variables = self.input_variables + additional_inputs

        prompt = PromptTemplate(template= Prompts.GenericComponentDesignerPrompt,
                                input_variables=self.input_variables)
        self.__llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=verbose)

    
    def design(self,
               component : Component,
               cloud_provider : str = 'Any',
               additional_input : Dict[str,str] = None):

        if component.component_type in ['Storage', 'Service']:
            raise ValueError('''This Designer is suitable for generic Components only. 
            Use StorageComponentDesigner or ServiceComponentDesigner as per component type.''')
        
        if cloud_provider not in ['AWS', 'Azure', 'GCP', 'Any']:
            raise ValueError("Cloud Provider should be from ['AWS', 'Azure', 'GCP', 'Any']")
        
        # validate input variables
        for var in self.input_variables:
            if var not in ['component', 'cloud_provider']:
                if additional_input is None or var not in additional_input.keys():
                    raise ValueError(f"input {var} is not provided.")

        
        inputs = { 'component' : str(component),
                    'cloud_provider' : cloud_provider,
        }
        if additional_input is not None:
            for var in additional_input.keys():
                inputs[var] = additional_input[var]

        output = self.__llm_chain.run(**inputs)
        return output
    
    def get_request_count(self):
        return 1