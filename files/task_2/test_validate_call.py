from pydantic import ValidationError
from files.task_2.validate_call import my_func, InputModel


def test_validate_call() -> None:
    print('Валидация №1 с корректными данными')
    try:
        data_model = InputModel(id='1', name='user')
        print(my_func(data_model))
    except ValidationError as e:
        print(e)
    finally:
        print('Валидация №1 произведена!')

    try:
        print('Валидация №2 с некорректными данными')
        data_model = InputModel(id='один', name='user')
        print(my_func(data_model))
    except ValidationError as e:
        print(e)
    finally:
        print('Валидация №2 произведена!')










