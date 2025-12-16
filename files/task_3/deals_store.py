"""База Данных"""""
from typing import List

from files.task_3.schemas import Deal


class DescriptorStore:
    def __init__(self):
        self.__storage = []

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        raise AttributeError("Direct access to 'db' is запрещён. "
                             "Используйте get_store() или set_store_data().")

    def __set__(self, instance, value):
        raise AttributeError("Direct assignment to 'db' is запрещён.")

    # служебные методы
    def get(self):
        return self.__storage

    def set(self, value: List):
        self.__storage = value


class DealsStore:
    _instance = None
    db = DescriptorStore()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_store(self):
        return type(self).db.get()

    def set_store(self, value: List[Deal]):
        type(self).db.set(value)


# # проверка работы модуля
# if __name__ == '__main__':
#     s1 = DealsStore()
#     s2 = DealsStore()
#
#     print(s1 is s2)           # True

