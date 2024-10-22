from pathlib import Path

class TextFile:

    def __init__(self,filepath):
        self.filename = filepath
        self.__file = None

    def __enter__(self):
        try:
            self.__file = open(self.filename, 'r+t')
        except FileNotFoundError:
            Path("data/").mkdir(parents=True, exist_ok=True)
            self.__file = open(self.filename, 'x+t')
        except TypeError:
            Path("data/").mkdir(parents=True, exist_ok=True)
            self.__file = open(f"data/{__name__}.txt", 'w+t')
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
        
        return [line.rstrip() for line in self.__file]
        
    # Saves from list to file
    def save(self,input_list: list[str]) -> bool:
        if self.__file is None:
            with self as fh:
                return fh.save(input_list)
        
        for item in input_list:
            self.__file.write(f"{item}\n")
        
        return True