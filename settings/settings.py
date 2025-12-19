import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'myDataBase1'
    DB_PASS: str = '12345'
    DB_NAME: str = 'postgres'

    @property
    def db_address(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}')

    model_config = SettingsConfigDict(
        extra="allow",
        env_file_encoding="utf-8",
        # env_file=os.path.abspath(os.path.join(BASE_DIR, ".env")),
        env_file=os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                ".env"))
    )










# # проверка работы модуля
# if __name__ == '__main__':
#     # Проверка работы файла settings.py
#     print("--- Текущие настройки ---")
#     print(f"DB_HOST: {settings.DB_HOST}")
#     print(f"DB_PORT: {settings.DB_PORT}")
#     print(f"DB_USER: {settings.DB_USER}")
#     print(f"DB_NAME: {settings.DB_NAME}")
#     # Осторожно: не выводите пароли в лог/консоль в реальных приложениях
#     print(f"DB_PASS: {settings.DB_PASS}")
#     print("-------------------------")
#
#     print(settings.db_adress)





