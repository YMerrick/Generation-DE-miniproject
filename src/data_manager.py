from abc import ABC, abstractmethod
from typing import Iterable

class DataManagerInterface(ABC):

    @abstractmethod
    def add(self):
        raise NotImplementedError()

    @abstractmethod
    def update(self):
        raise NotImplementedError()

    @abstractmethod
    def delete_element(self):
        raise NotImplementedError()

class StrListDataManager(DataManagerInterface):
    def __init__(self, input_list: list[str]):
        super().__init__()
        self.user_list = input_list

    def add(self, new_input):
        self.user_list.append(new_input)
        return self.user_list

    def update(self, index, new_input):
        self.user_list[index] = new_input
        return self.user_list[index]

    def delete_element(self, index):
        return self.user_list.pop(index - 1)

    def get_data(self) -> list[str]:
        return self.user_list

class DictDataManager(DataManagerInterface):

    def __init__(self, input_list: list[dict]):
            super().__init__()
            self.user_list = input_list

    def add(self, new_dict):
        self.user_list.append(new_dict)

    def update(self, user_selection: int, property_selected: str, updated_property: str) -> dict:
        selected_dict = self.user_list[user_selection - 1]
        selected_dict[property_selected] = updated_property
        return selected_dict

    def delete_element(self, user_selection: int) -> dict:
        return self.user_list.pop(user_selection)

    def get_keys(self) -> Iterable | None:
        if self.user_list:
            return list(self.user_list[0].keys())
        return None

    def get_data(self) -> list[dict]:
        return self.user_list

    def get_length(self) -> int:
        return len(self.user_list)