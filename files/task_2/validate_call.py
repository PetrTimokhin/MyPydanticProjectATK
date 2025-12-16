from pydantic import validate_call, BaseModel, ValidationError


class InputModel(BaseModel):
    id: int
    name: str


@validate_call()
def my_func(value: InputModel) -> str:
    return f'id: {value.id}, name: {value.name}'






