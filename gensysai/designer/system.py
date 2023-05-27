from langchain.llms import BaseLLM
from .storage import StorageComponentDesigner
from .service import ServiceComponentDesigner
from .designer import GenericComponentDesigner
from .analyzer import ProblemAnalyzer
from .titlegen import TitleGenerator
from ..designdoc import DesignedComponent, DesignDocument
import time

SLEEP_TIME_IN_SECONDS = 65

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
        self.title_generator = TitleGenerator(llm=llm, verbose=verbose)
        self.design_doc = None
        self.verbose = verbose

        # OpenAI request tracker
        self.track_request = True
        self.current_request_count = 0

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

        self.design_doc = DesignDocument()
        self.design_doc.title = self.title_generator.generate_title(problem_statement)
        self.design_doc.problem_statement = problem_statement
        self.current_request_count += self.title_generator.get_request_count()

        try:
            system = self.problem_analyzer.analyze(problem=problem_statement)
        except Exception as e:
            raise ValueError(f"Sorry. It does not seem like a valid system design problem. Please rephrase your question.")
        
        self.current_request_count += self.problem_analyzer.get_request_count()
        self._debug("Problem analysis is completed...")

        self.design_doc.functional_requirement = system.functional_requirements

        # Wait as OpenAI apis are ratelimited
        self.wait_if_tracked()


        ## TODO: algorithm for ordered components
        # design services first and then the storage.
        for component in system.components:
            designed_component = DesignedComponent()
            designed_component.name = component.name
            self._debug(f"Design started for component {component.name}.")

            if component.component_type == "Storage":
                design = self.storage_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = design
                self.current_request_count += self.storage_designer.get_request_count()
            
            elif component.component_type == "Service":
                design = self.service_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = str(design)
                self.current_request_count += self.service_designer.get_request_count()

            else:
                design = self.misc_designer.design(component=component, cloud_provider=self.cloud_provider)
                designed_component.design = design
                self.current_request_count += self.misc_designer.get_request_count()

            # Wait as OpenAI apis are ratelimited
            self.wait_if_tracked()

            self.design_doc.components.append(designed_component)
            self._debug(f"Design for component {component.name} is completed.")
            

        self._debug("System Design completed...\n")
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
            file.write(self.generate_markdown())
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

    def wait_if_tracked(self):
        
        if self.track_request and self.current_request_count % 3 == 0:
            self._debug(f"Total request : {self.current_request_count}, Sleep for {SLEEP_TIME_IN_SECONDS} seconds")
            time.sleep(SLEEP_TIME_IN_SECONDS)