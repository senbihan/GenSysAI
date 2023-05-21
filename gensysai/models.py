from pydantic import BaseModel, Field, validator
from typing import List

class Component(BaseModel):
    '''Represents a single component of a system'''

    name: str = Field(description="name of the component")
    description: str = Field(description="description of the component")
    component_type: str = Field(description="type of the component")
    
    # # You can add custom validation logic easily with Pydantic.
    # @validator('component_type')
    # def component_type_validation(cls, field):
    #     if field not in ['Storage', 'Service', 'Load Balancer', 'Cache', 'Database']:
    #         raise ValueError(f'not a valid component : {field}')
    #     return field

    def __str__(self) -> str:
        return f'''{{
            "name" : {self.name},
            "component_type" : {self.component_type},
            "description" : {self.description}
        }}'''

class System(BaseModel):
    '''Represents a System that consists of multiple components'''

    functional_requirements : str = Field(description="Functional Requirements")
    components: List[Component] = Field(description="List of Components")

class ServiceComponent(BaseModel):
    '''Represents a Service Component with a design'''
    requirement: str = Field(description="Requirements of the service component")
    apis: List[str] = Field(description="apis of the service")
    conclusion: str = Field(description="overall conclusions on the component")

    def __str__(self) -> str:
        apistr = '\t'
        for api in self.apis:
            apistr += api + '\n\t'
        return f'''#### Requirements:\n{self.requirement}\n#### APIs\n{apistr}\n#### Comments\n{self.conclusion}\n'''