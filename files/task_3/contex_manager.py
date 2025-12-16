"""Контекстный менеджер БД """
from files.task_3.deals_store import DealsStore
from settings.settings import Settings


class ContextManagerDB:
    def __init__(self):
        self.settings = Settings()

    def __enter__(self) -> DealsStore:
        print(f"[DB CONNECT] присоединение к {self.settings.db_adress}")
        print("[DB CONNECT] соединение установлено!")
        return DealsStore()

    def __exit__(self, exc_type, exc, tb):
        print(f"[DB DISCONNECT] отсоединение от {self.settings.db_adress}")
        print("[DB DISCONNECT] соединение закрыто!")



# # Проверка работы модуля
# if __name__ == '__main__':
#     with ContextManagerDB() as db:
#         print(db.get_store())