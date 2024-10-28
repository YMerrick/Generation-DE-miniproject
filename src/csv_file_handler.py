from pathlib import Path
from csv import DictReader, DictWriter

class CSVFile:

    def __init__(self, filepath: str):
        self.filename = filepath

    def load(self) -> list[dict]:       
        new_list: list[dict]
        with open(self.filename, 'rt') as file:
            # Implement loading function here
            reader = DictReader(file)
            new_list = [row for row in reader]
        return new_list


    def save(self, input_list: list[dict]) -> None:
        with open(self.filename, 'wt') as file:
            # Implement saving function here
            column_headers = [header for header in input_list[0].keys()]
            writer = DictWriter(file, fieldnames=column_headers, lineterminator='\r')
            writer.writeheader()
            writer.writerows(input_list)
            