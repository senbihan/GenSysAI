from langchain.llms import BaseLLM
from ..models import System
from langchain.output_parsers import PydanticOutputParser
from langchain import PromptTemplate, LLMChain
from ..prompts import Prompts
from ..chains import ComponentIdenfierChain
from .openaioperation import OpenAIOperation

class ProblemAnalyzer(OpenAIOperation):
    '''Given a problem statement declaring a system to be designed
    , it analyzes and identifies the components of the systems'''

    def __init__(self, 
            llm : BaseLLM,
            verbose : bool = False) -> None:
        self.llm = llm
        self.verbose = verbose
        self.__parser : PydanticOutputParser = PydanticOutputParser(pydantic_object=System)
        self.__build_chain()


    def __build_chain(self) -> None:
        
        # chain for functional requirement identification
        __prompt_functional_requirement = PromptTemplate(template=Prompts.FunctionalRequirementPrompt, 
                                input_variables=["input"])
        self.__chain_func_requirement = LLMChain(prompt=__prompt_functional_requirement,
                                llm= self.llm,
                                verbose=self.verbose)
        

        # Chain for component identification
        __prompt_component_identify = PromptTemplate(template=Prompts.ComponentIdentifierPrompt, 
                        input_variables=["input"],
                        partial_variables={"format_instructions": self.__parser.get_format_instructions()}
                    )
        self.__chain_component_identify = LLMChain(prompt=__prompt_component_identify,
                                    llm = self.llm,
                                    verbose= self.verbose)
        

        # Component idenfication chain
        self.combined_chain = ComponentIdenfierChain(
                        chains=[self.__chain_func_requirement, self.__chain_component_identify], 
                        chained_input_key='input', 
                        verbose=self.verbose)


    def analyze(self, problem : str) -> System:
        
        analyzed_output = self.combined_chain(problem, return_only_outputs=True)
        designed_system = self.__parser.parse(analyzed_output['output'])
        designed_system.functional_requirements = analyzed_output['chain_0']

        return designed_system
    
    def get_request_count(self):
        return 2
    