from __future__ import annotations

import typing
from pydantic import BaseModel, Field, root_validator
from pydantic.generics import GenericModel
from datetime import datetime


class DbConnection(typing.Protocol):
    async def commit(self):
        raise NotImplementedError()

    async def rollback(self):
        raise NotImplementedError()

    async def transaction(self):
        raise NotImplementedError()

    async def execute(self, query, values=None):
        raise NotImplementedError()

    async def execute_many(self, query, values):
        raise NotImplementedError()

    async def fetch_all(self, query):
        raise NotImplementedError()

    async def fetch_one(self, query):
        raise NotImplementedError()

    async def fetch_val(self, query):
        raise NotImplementedError()


class PageInfo(BaseModel):
    start_cursor: datetime
    end_cursor: datetime
    has_next_page: bool
    has_previous_page: bool


class Edges(BaseModel):
    cursor: str
    node: typing.Any

    class Config:
        use_enum_values = True


class PaginatedResource(GenericModel):
    page_info: PageInfo
    edges: typing.List[Edges]


class SearchType(BaseModel):
    value: typing.Union[int, str]
    columns: typing.List[str]


class PaginationParams(BaseModel):
    first: int = None
    after: datetime = None
    after_with: typing.Optional[datetime]
    last: int = None
    before: datetime = None
    before_with: typing.Optional[datetime]
    q: typing.Optional[str]
    sort: typing.Optional[str]
    order: typing.Literal["asc", "desc"] = Field("asc")

    search: typing.Optional[SearchType]
    filter: typing.Optional[
        typing.List[typing.Dict[str, typing.Union[str, int]]]
    ]

    class Config:
        allow_mutation = False
        extra = "ignore"

    @root_validator
    def check_valid_pagination(cls, values):
        first, after, after_with = (
            values.get("first"),
            values.get("after"),
            values.get("before_with"),
        )
        last, before, before_with = (
            values.get("last"),
            values.get("before"),
            values.get("before_with"),
        )
        forward = first or after or after_with
        backward = last or before or before_with

        if forward or backward:
            return values
        elif forward and backward:
            raise ValueError("Paging can't be forward and backward")
        else:
            raise ValueError("Invalid paging params")
