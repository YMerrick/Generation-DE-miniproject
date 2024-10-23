from pathlib import Path

class TextFile:

    def __init__(self,filepath,* ,mode = 'r+t', **kwargs):
        self.filename = filepath
        self.__file = None
        self.__mode = mode
        self.__kwargs = kwargs

    def __enter__(self):
        try:
            self.__file = open(self.filename, self.__mode, **self.__kwargs)
        except FileNotFoundError:
            Path("data/").mkdir(parents=True, exist_ok=True, **self.__kwargs)
            self.__file = open(self.filename, 'x+t')
        except TypeError:
            Path("data/").mkdir(parents=True, exist_ok=True, **self.__kwargs)
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