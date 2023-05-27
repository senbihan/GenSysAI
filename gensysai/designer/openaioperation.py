from abc import ABC, abstractmethod

class OpenAIOperation(ABC):

    ''' Abstract class for for any operation that uses OpenAI '''
    @abstractmethod
    def get_request_count(self) -> int:
        return 0