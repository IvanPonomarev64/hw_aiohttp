import pydantic
from exception import HTTPError


class OwnerModel(pydantic.BaseModel):
    email: str
    password: str


class AdvertisementModel(pydantic.BaseModel):
    title: str
    description: str
    token: str


def validator_model(data: dict, model):
    try:
        return model(**data).dict()
    except pydantic.ValidationError as error:
        raise HTTPError(400, error.errors())
