from typing import List

class DesignedComponent:
    name : str
    design : str

class DesignDocument:
    title : str
    problem_statement : str
    functional_requirement: str
    components : List[DesignedComponent] = []

