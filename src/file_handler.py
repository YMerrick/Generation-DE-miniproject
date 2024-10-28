from abc import ABC, abstractmethod

class MyFileHandler(ABC):
    
    def __init__(self, filepath):
        super().__init__()
        self.filename = filepath

    @abstractmethod
    def load() -> list:
        pass

    @abstractmethod
    def save() -> bool:
        pass