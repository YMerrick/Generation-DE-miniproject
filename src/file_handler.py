from abc import ABC, abstractmethod
from pathlib import Path
from csv import DictReader, DictWriter

class DataHandler(ABC):
   
    @abstractmethod
    def load() -> list:
        raise NotImplementedError()

    @abstractmethod
    def save() -> bool:
        raise NotImplementedError()

class MyFileHandler(DataHandler):
    
    def __init__(self, filepath):
        super().__init__()
        self.filename = filepath

class TextFile(MyFileHandler):

    def __init__(self,filepath, *, mode = 'r+t', **kwargs):
        super().__init__(filepath)
        self.__file = None
        self.__mode = mode
        self.__kwargs = kwargs

    def __enter__(self):
        try:
            self.__file = open(self.filename, self.__mode, **self.__kwargs)
        except FileNotFoundError:
            Path("data/").mkdir(parents=True, exist_ok=True)
            self.__file = open(self.filename, 'x+t', **self.__kwargs)
        except TypeError:
            Path("data/").mkdir(parents=True, exist_ok=True)
            self.__file = open(f"data/{__name__}.txt", 'w+t', **self.__kwargs)
        except Exception as ex:
            print(ex)
        return self

    def __exit__(self, *args):
        self.__file.close()

    def __del__(self):
        if self.__file:
            self.__file.close()

    # Reads from file and then return list of products
    def load(self) -> list[str]:
        if self.__file is None:
            with self as fh:
                return fh.load()
        
        return [line.rstrip() for line in self.__file if line.rstrip()]
        
    # Saves from list to file
    def save(self,input_list: list[str]) -> bool:
        if self.__file is None:
            with self as fh:
                return fh.save(input_list)
        
        was_closed = self.__file.closed
        if was_closed:
            self.__file = open(self.filename, 'wt')

        self.__file.write('\n'.join(input_list))

        if was_closed:
            self.__file.close()

        return True
    
class CSVFile(MyFileHandler):

    def __init__(self, filepath: str):
        super().__init__(filepath)

    def load(self) -> list[dict]:       
        '''This takes the file and returns a list of dictionaries
        
        the keys are the headers and the value is the data'''
        new_list: list[dict]
        with open(self.filename, 'rt') as file:
            # Implement loading function here
            reader = DictReader(file)
            new_list = [row for row in reader]
        return new_list

    def save(self, input_list: list[dict], template: dict = None) -> bool:
        if len(input_list) < 1 and template is None:
            return False

        with open(self.filename, 'wt') as file:
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
        with open(self.filename, 'rt') as file:
            header_row = file.readline()
            header_list = [header.rstrip() for header in header_row.split(',')]
        
        return header_list