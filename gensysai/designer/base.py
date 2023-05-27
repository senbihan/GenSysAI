from abc import ABC, abstractmethod
from typing import Dict, Any
from ..models import Component


class BaseComponentDesigner(ABC):
    ''' Abstract class for Component Designer '''
    @abstractmethod
    def design(self, 
               component : Component, 
               cloud_provider : str = 'Any',
               additional_input : Dict[str,str] = None) -> Any:
        pass