"""Модели Pydantic"""

from datetime import datetime
import re
from enum import Enum, auto
from typing import Any, Optional

from pydantic import BaseModel, Field, EmailStr, field_validator, \
    computed_field, ConfigDict


class IdCounterUser:
    """Хранит и инкрементирует последнее использованное ID для класса User."""
    current_id: int = 0

    @classmethod
    def get_next_id(cls) -> int:
        cls.current_id += 1
        return cls.current_id


class IdCounterDeal:
    """Хранит и инкрементирует последнее использованное ID для класса Deal."""
    current_id: int = 0

    @classmethod
    def get_next_id(cls) -> int:
        cls.current_id += 1
        return cls.current_id


def to_camel(snake_str: str) -> str:
    """Конвертирует snake_case в camelCase."""
    components = snake_str.split('_')
    # Соединяем части, оставляя первую как есть (или делая ее строчной)
    return components[0] + ''.join(x.title() for x in components[1:])


class User(BaseModel):
    """Модель валидации пользователей User"""
    id: int | None = Field(default_factory=IdCounterUser.get_next_id, title='id', description='id пользователя')
    name: str = Field(..., title='имя пользователя', description='имя пользователя')
    user_name: str | None = Field(default=None, title='имя пользователя user_name', description='имя пользователя user_name')
    age: int = Field(default=None, ge=0, title='возраст', description="возраст пользователя")
    is_supervisor: bool = Field(default=False, title='имя пользователя', description='имя пользователя')
    email: EmailStr | None = Field(default=None, title='email', description="адресс эл. почты")
    # phone_number: str = Field(default=None, title='телефон', description='телефон пользователя')  # вариант с @field_validator
    phone_number: str | None = Field(default=None,
                              pattern=r"^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$",  # вариант через pattern
                              title='телефон',
                              description='телефон пользователя')

    # # model_config без ConfigDict
    # model_config = {
    #     "alias_generator": to_camel,
    #     # Используем нашу функцию to_camel() для генерации псевдонимов
    #     "populate_by_name": True,
    #     # Позволяет устанавливать поля по snake_case или camelCase (по желанию)
    # }

    # # model_config с ConfigDict
    model_config = ConfigDict(
        # Используем нашу функцию to_camel() для генерации псевдонимов
        alias_generator=to_camel,
        # Позволяет устанавливать поля по snake_case или camelCase (по желанию)
        populate_by_name=True)

    def model_post_init(self, __context: Any) -> None:
        """Вызывается после того, как все поля были инициализированы
        (включая id и name)."""
        if self.user_name is None:
            # Если username не был передан явно, генерируем его
            self.user_name = f"{self.id}_{self.name}"

    # # Заменил на pattern в Field
    # @field_validator("phone_number", mode='before')
    # @classmethod
    # def validate_phone_number(cls, values: str) -> str:
    #     """Валидация поля phone_number через @field_validator"""
    #     if not re.match(r"^\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}$", values):
    #         raise ValueError('Номер телефона должен соответствовать схеме'
    #                          ' +7 (000) 000-00-00')
    #     return values


class DealType(Enum):
    """Класс - описывающий тип сделки (перечисление)"""
    buy = auto()
    sale = auto()


class Deal(BaseModel):
    """Модель валидации сделок Deal"""
    id: int = Field(default_factory=IdCounterDeal.get_next_id, title='id', description='id сделки')
    title: str = Field(title='заголовок сделки', description='заголовок')
    comment: str | None = Field(default='нет комментария', title='комментарий', description='комментарий')
    created_at: datetime = Field(..., title='время', description='время создания сделки') # не раньше сегодня
    persons_in_charge: list[User] = Field(title='список пользователей', description='список пользователей сделки') # list[User]
    deal_type: DealType = Field(default=None, title='тип сделки', description='тип сделки')

    @field_validator('created_at')
    @classmethod
    def check_created_at_not_in_future(cls, value: datetime) -> datetime:
        """Проверяет, что дата создания не находится в будущем."""
        today = datetime.now()

        if value > today:
            raise ValueError(
                f"Дата создания ({value}) позже текущего времени ({today})")
        return value

    @field_validator("created_at", mode="before")
    def parse_date(cls, v):
        """Ф-ция позволяет использовать время в удобном формате = день.месяц.год"""
        if isinstance(v, str):
            return datetime.strptime(v, "%d-%m-%Y")
        return v


# # проверка работы модуля
# if __name__ == '__main__':
#     deal_json_1 = ('{"title": "Сделка",'
#                    ' "comment": "Коммент",'
#                    ' "created_at": "10-10-2025",'
#                    ' "persons_in_charge": [{"name": "Petr", "age": 43, "email": "petr@example.com", "phone_number": "+7 (000) 000-00-00"}],'
#                    ' "deal_type": 1}')
#     deal_1_from_json = Deal.model_validate_json(deal_json_1)
#     print(deal_1_from_json)


    # print(DealType.buy.value)
    # print(DealType.sale.value)
    # print(DealType.buy.name)

    # data_json = '{"name": "Petr", "age": 43, "email": "alice@example.com", "phone_number": "+7 (925) 333-33-33"}'
    # print(User.model_validate_json(data_json))
    # print(User.model_validate_json(data_json))
    # print(User.model_validate_json(data_json))
    # user1_from_json = User.model_validate_json(data_json)
    # print(user1_from_json.model_dump(by_alias=True))

