"""
"""
from __future__ import annotations

import typing
from datetime import datetime
from .types import DbConnection
from .utils import get_column, as_dict
from .query_builder import query_builder
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.selectable import Selectable
from .types import (
    PaginationParams,
    PageInfo,
    PaginatedResource,
    Edges,
)
from .exceptions import PaginationError


class CursorPagination(object):
    """
    parameters:
    query: query to execute
    db_conn: database connection
    node_model: model to format data node
    """

    def __init__(
        self,
        db_conn: DbConnection,
        query: Selectable = None,
        node_model=None,
        cursor_column="created_on",
    ):
        self.db = db_conn
        self.query = None
        self.cursor_column = cursor_column
        self.node_model = node_model
        self._query = query

    async def resource(self, params: PaginationParams):
        limit = self.page_limit(params)
        if limit:
            return await self.db.fetch_all(query=self.query.limit(limit))
        else:
            return await self.db.fetch_all(self.query)

    async def page(self, params: PaginationParams):
        paging = self.paging_direction(params)
        self.query = query_builder(self._query, params, self.cursor_column)
        edges = await self.edges(params)
        start_cursor = self.__start_cursor(edges)
        end_cursor = self.__end_cursor(edges)

        if paging == "backward":
            has_next_page = await self.__has_previous(params, start_cursor)
            has_previous_page = await self.__has_next(params, end_cursor)
        else:
            has_next_page = await self.__has_next(params, end_cursor)
            has_previous_page = await self.__has_previous(params, start_cursor)
        return PaginatedResource.construct(
            edges=edges,
            page_info=PageInfo.construct(
                start_cursor=start_cursor,
                end_cursor=end_cursor,
                has_next_page=has_next_page,
                has_previous_page=has_previous_page,
            ),
        )

    async def edges(self, params: PaginationParams):
        resource = await self.resource(params)
        paging = self.paging_direction(params)
        if self.db.url.dialect == "sqlite":
            columns = [c.name for c in self.query.columns]
            resource = as_dict(resource, columns)
        edges = [
            Edges.construct(
                cursor=node.get(self.cursor_column, None),
                node=self.__node(node),
            )
            for node in resource
        ]

        if paging == "backward":
            edges.reverse()
        return edges

    def __start_cursor(self, edges: typing.List[Edges]):
        try:
            return edges[0].cursor
        except Exception:
            return None

    def __end_cursor(self, edges: typing.List[Edges]):
        try:
            return edges[-1].cursor
        except Exception:
            return None

    def __node(self, node):
        if self.node_model:
            return self.node_model(**dict(node))
        return dict(node)

    async def __has_next(self, params: PaginationParams, beyond: datetime):
        before = params.before
        query = self.query.alias("alias")
        if beyond is None:
            if before is None:
                return False
            beyond = before
        cursor = get_column(query, self.cursor_column)
        beyond_the_limit = await self.db.fetch_all(
            query=select([query]).where(cursor < beyond)
        )
        return bool(beyond_the_limit)

    async def __has_previous(self, params: PaginationParams, beyond: datetime):
        after = params.after
        query = self.query.alias("alias")
        if beyond is None:
            if after is None:
                return False
            beyond = after
        cursor = get_column(query, self.cursor_column)
        beyond_the_limit = await self.db.fetch_all(
            query=select([query]).where(cursor > beyond)
        )
        return bool(beyond_the_limit)

    def __enter__(self):
        return self

    def __exit__(self, typ, value, traceback):
        pass

    def _get_column(self, name):
        return getattr(self._query.c, name)

    @staticmethod
    def paging_direction(params: PaginationParams):
        first = params.first
        last = params.last
        after = params.after
        before = params.before
        after_with = params.after_with
        before_with = params.before_with

        if after or first or after_with:
            return "forward"
        elif before or last or before_with:
            return "backward"
        else:
            raise PaginationError("Invalid paging parameters")

    @staticmethod
    def page_limit(params: PaginationParams):
        return params.first or params.last
