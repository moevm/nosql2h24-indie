from pydantic import BaseModel


class Place(BaseModel):
    name: str
    type: str
    address: str
    phone_master: str
