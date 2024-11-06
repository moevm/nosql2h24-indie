from pydantic import BaseModel, Field
from arango.typings import Json


class Place(BaseModel):
    name: str
    type: str
    address: str
    phone_number: str


class File(BaseModel):
    content: Json


class GroupAnnouncement(BaseModel):
    group_id: str
    announcement: Json


class UserAnnouncement(BaseModel):
    user_id: str
    announcement: Json


class Comment(BaseModel):
    user_id: str
    announcement_id: str
    comment: Json


class Star(BaseModel):
    From: str = Field(alias="from")
    to: str


class Group(BaseModel):
    name: str
