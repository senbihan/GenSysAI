from langchain.llms import BaseLLM
from .models import Component, ServiceComponent
from langchain import PromptTemplate, LLMChain
from .prompts import Prompts
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .analyzer import ProblemAnalyzer
from .designdoc import DesignedComponent, DesignDocument
from langchain.output_parsers import PydanticOutputParser
import time

SLEEP_TIME_IN_SECONDS = 61

class BaseComponentDesigner(ABC):
    ''' Abstract class for Component Designer '''
    @abstractmethod
    def design(self, 
               component : Component, 
               cloud_provider : str = 'Any',
               additional_input : Dict[str,str] = None) -> Any:
        pass

class StorageComponentDesigner(BaseComponentDesigner):
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
    


class ServiceComponentDesigner(BaseComponentDesigner):
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
            raise ValueError("This Designer is suitable for Storage Components only")
        
        output = self.__llm_chain.run(component = str(component))
        return self.__parser.parse(output)
    

class GenericComponentDesigner(BaseComponentDesigner):
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
            raise ValueError("This Designer is suitable for Storage Components only")
        
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
    

class SystemDesigner:

    ''' The SystemDesigner class handles the entire design of the system '''

    def __init__(self,
            llm : BaseLLM ,
            cloud_provider : str = "Any",
            problem_analyzer : ProblemAnalyzer = None,
            storage_designer : StorageComponentDesigner = None,
            service_designer : ServiceComponentDesigner = None,
            misc_designer : GenericComponentDesigner = None,
            verbose: bool = False
            ) -> None:
        """
        Initialize the SystemDesigner object.

        Args:
            llm (BaseLLM): The BaseLLM object. \n
            cloud_provider (str, optional): The cloud provider. Defaults to "Any". \n
            problem_analyzer (ProblemAnalyzer, optional): The ProblemAnalyzer object. Defaults to None. \n
            storage_designer (StorageComponentDesigner, optional): The StorageComponentDesigner object. Defaults to None. \n
            service_designer (ServiceComponentDesigner, optional): The ServiceComponentDesigner object. Defaults to None. \n
            misc_designer (GenericComponentDesigner, optional): The GenericComponentDesigner object. Defaults to None.\n
            verbose (bool, optional): Verbose mode flag. Defaults to False.\n
        """

        self.llm = llm
        self.cloud_provider = cloud_provider
        self.problem_analyzer = problem_analyzer if problem_analyzer is not None else ProblemAnalyzer(llm=self.llm, verbose=verbose)
        self.storage_designer = storage_designer if storage_designer is not None else StorageComponentDesigner(llm=self.llm, verbose=verbose) 
        self.service_designer = service_designer if service_designer is not None else ServiceComponentDesigner(llm=self.llm, verbose=verbose) 
        self.misc_designer = misc_designer if misc_designer is not None else GenericComponentDesigner(llm=self.llm, verbose=verbose) 
        self.design_doc = None
        self.verbose = verbose

    def design(self, 
            problem_statement : str
            ) -> str:
        """
        Design the system based on the provided problem statement.

        Args:
            problem_statement (str): The problem statement.

        Returns:
            str: The design document.
        """

        request_count = 0
        self.design_doc = DesignDocument()
        system = self.problem_analyzer.analyze(problem=problem_statement)
        
        # Problem analyzer makes 2 requests to OpenAI
        request_count += 2
        
        self.design_doc.title = "DESIGN DOC" # TODO: LLM based title generation?
        self.design_doc.problem_statement = problem_statement
        self.design_doc.functional_requirement = system.functional_requirements

        for component in system.components:
            designed_component = DesignedComponent()
            designed_component.name = component.name
            self._debug(f"Design started for component {component.name}.")

            if component.component_type == "Storage":
                design = self.storage_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = design
            
            elif component.component_type == "Service":
                design = self.service_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = str(design)

            else:
                design = self.misc_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = design

            self.design_doc.components.append(designed_component)
            self._debug(f"Design for component {component.name} is completed.")
            request_count += 1

            if request_count % 3 == 0:
                time.sleep(SLEEP_TIME_IN_SECONDS)
                self._debug(f"Sleep for {SLEEP_TIME_IN_SECONDS} seconds")

        self._debug("Design complete!")
        return self.design_doc

    def dump_to_md_file(self, path : str):
        """
        Dumps the Generated design to a markdown file

        Args:
            path (str): The pathstring of a markdown file, should end with `.md`

        Returns:
            None: 
        """
        if path[-2:] != 'md':
            raise ValueError("The path should be a valid markdown file")
        
        if self.design_doc is None:
            raise ValueError("Design doc is not generated yet. Run `design()` to generate a design doc")
        
        with open(path, 'w') as file:
            file.write(f"# {self.design_doc.title}")
            file.write("\n\n\n\n")

            file.write(f'## Problem Statement')
            file.write("\n\n")
            file.write(f'{self.design_doc.problem_statement}')
            file.write("\n\n")

            file.write(f'## Functional Requirements')
            file.write("\n\n")
            file.write(f'{self.design_doc.functional_requirement}')
            file.write("\n\n")

            file.write(f'## Components')
            file.write("\n\n")
            for component in self.design_doc.components:
                file.write(f'### {component.name}')
                file.write("\n")
                file.write(f'{component.design}')
                file.write("\n\n")

        file.close()
    
    def generate_markdown(self):
        """
        Generates a markdown file of the design
        """
        if self.design_doc is None:
            raise ValueError("Design doc is not generated yet. Run `design()` to generate a design doc")
        
        design = ''
        design += f"# {self.design_doc.title}\n\n\n\n"
        design += f'## Problem Statement\n\n'
        design += f'{self.design_doc.problem_statement}\n\n'
        design += f'## Functional Requirements\n\n'
        design += f'{self.design_doc.functional_requirement}\n\n'
        design += f'## Components\n\n'
        for component in self.design_doc.components:
            design += f'### {component.name}\n'
            design += f'{component.design}\n\n'

        return design

    def _debug(self, message):
        if self.verbose :
            print(message)