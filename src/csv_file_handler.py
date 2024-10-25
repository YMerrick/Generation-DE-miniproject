from pathlib import Path

class CSVFile:

    def __init__(self, filepath: str, **kwargs):
        self.filename = filepath
        self.__file = None
        self.__open_kwargs = kwargs


    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        if self.__file:
            self.__file.close()

    def __del__(self):
        if self.__file:
            self.__file.close()

    def load() -> list[dict]:
        pass

    def save(input_list: list[dict]) -> None:
        pass