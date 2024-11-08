from abc import ABC, abstractmethod
from pathlib import Path
from csv import DictReader, DictWriter
from typing import IO

class DataHandler(ABC):
   
    @abstractmethod
    def load(self) -> list:
        raise NotImplementedError()

    @abstractmethod
    def save(self) -> bool:
        raise NotImplementedError()

class MyFileHandler(DataHandler):
    
    def __init__(self, filepath: str):
        super().__init__()
        self.filename: str = filepath
    
class CSVFile(MyFileHandler):

    def __init__(self, filepath: str):
        super().__init__(filepath)

    def open_file(self, **kwargs) -> IO:
        '''This opens attempts to open and then return a file from the instance attribute'''
        try:
            file = open(self.filename, **kwargs)
        except FileNotFoundError:
            Path('/'.join(self.filename.split('/')[:-1])).mkdir(parents=True, exist_ok=True)
            Path(self.filename).touch(exist_ok=True)
            file = open(self.filename, **kwargs)
        except Exception:
            print("Unexpected error found")
            raise
        return file

    def load(self) -> list[dict]:       
        '''This takes the file and returns a list of dictionaries
        
        the keys are the headers and the value is the data'''
        new_list: list[dict]
        with self.open_file(mode='rt') as file:
            # Implement loading function here
            reader = DictReader(file)
            new_list = [row for row in reader]
        return new_list

    def save(self, input_list: list[dict], template: dict = None) -> bool:
        if len(input_list) < 1 and template is None:
            return False

        with self.open_file(mode='wt') as file:
            column_headers: list
            # Implement saving function here
            if template:
                column_headers = [header for header in template.keys()]
            else:
                column_headers = [header for header in input_list[0].keys()]
            writer = DictWriter(file, fieldnames=column_headers, lineterminator='\r')
            writer.writeheader()
            writer.writerows(input_list)

        return True

    def get_headers(self) -> list[str]:
        header_list: list[str]
        with self.open_file(mode='rt') as file:
            header_row = file.readline()
            header_list = [header.rstrip() for header in header_row.split(',')]
        
        return header_list