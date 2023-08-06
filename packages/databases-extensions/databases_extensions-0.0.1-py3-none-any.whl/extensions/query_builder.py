"""
advanced query builder for filters and sorting
"""

from datetime import datetime
from typing import Any, Dict, List, Union, Literal
from .types import PaginationParams
from .utils import change_camel_case_to_snake, parse_filter_value
import sqlalchemy as sa
from sqlalchemy.sql.selectable import Selectable

UNARY_OPERATORS = ["is_null", "is_not_null", "is_true", "is_false"]


def is_null(arg1: Any, arg2: Any = None):
    return arg1 == None  # noqa


def is_not_null(arg1: Any, arg2: Any = None):
    return arg1 != None  # noqa


def is_true(arg1: bool, arg2: Any = None):
    return arg1 == True  # noqa


def is_false(arg1: bool, arg2: Any = None):
    return arg1 != False  # noqa


def equals(arg1: Union[int, str, datetime], arg2: Union[int, str, datetime]):
    return arg1 == arg2


def not_equals(
    arg1: Union[int, str, datetime], arg2: Union[int, str, datetime]
):
    return arg1 != arg2


def ignore_case_equals(arg1: str, arg2: str):
    return sa.func.lower(arg1) == arg2.lower()


def greater_than(arg1: Union[int, datetime], arg2: Union[int, datetime]):
    return arg1 > arg2


def greater_than_equals(
    arg1: Union[int, datetime], arg2: Union[int, datetime]
):
    return arg1 >= arg2


def less_than(arg1: Union[int, datetime], arg2: Union[int, datetime]):
    return arg1 < arg2


def less_than_equals(arg1: Union[int, datetime], arg2: Union[int, datetime]):
    return arg1 <= arg2


def like(arg1: str, arg2: str):
    return arg1.like(arg2)


def not_like(arg1: str, arg2: str):
    return ~arg1.like(arg2)


def ilike(arg1: str, arg2: str):
    return arg1.ilike(arg2)


def not_ilike(arg1: str, arg2: str):
    return ~arg1.ilike(arg2)


def in_(arg1: Union[int, str], arg2: Union[int, str]):
    return arg1.in_(arg2)


def not_in(arg1: Union[int, str], arg2: Union[int, str]):
    return ~arg1.in_(arg2)


def contains(arg1: str, arg2: str):
    return arg1.contains(arg2)


OPERATORS = {
    # Unary operators.
    "is_null": is_null,
    "is_not_null": is_not_null,
    "is_true": is_true,
    "is_false": is_false,
    # Binary operators.
    "eq": equals,
    "ne": not_equals,
    "ieq": ignore_case_equals,
    "gt": greater_than,
    "lt": less_than,
    "gte": greater_than_equals,
    "lte": less_than_equals,
    "like": like,
    "not_like": not_like,
    "ilike": ilike,
    "not_ilike": not_ilike,
    "in": in_,
    "not_in": not_in,
    "contains": contains,
}


def get_column(query, name):
    try:
        snake = change_camel_case_to_snake(name)
        return query.c[snake]
    except KeyError:
        raise KeyError("column {} not found".format(name))


def query_builder(
    query: Selectable, params: PaginationParams, cursor: str = "created_on"
) -> Selectable:
    filters: List[Dict] = params.filter
    search: Dict = params.search
    sort: str = params.sort
    order: Literal["asc", "desc"] = params.order
    first, after, after_with = params.first, params.after, params.after_with
    before, before_with = params.before, params.before_with

    restrictions = []
    search_restrictions = []
    alias = query.alias("query")

    # Search clauses
    if search:
        for c in search.columns:
            col = get_column(alias, c)
            search_restrictions.append(col.ilike(f"%{str(search.value)}%"))
    # Filter clauses
    if filters:
        for f in parse_filter_value(filters):
            col = get_column(alias, f["name"])
            if f["operation"] in UNARY_OPERATORS:
                restrictions.append(OPERATORS[f["operation"]](col))
            else:
                restrictions.append(OPERATORS[f["operation"]](col, f["value"]))
    if search_restrictions:
        restrictions.append(sa.or_(*search_restrictions))

    if restrictions:
        selectable = sa.select([alias], whereclause=sa.and_(*restrictions))
    else:
        selectable = sa.select([alias])

    # Pagination
    cursor_column = get_column(alias, cursor)
    if first or after:
        selectable = selectable.order_by(cursor_column.desc())
        if after:
            selectable = selectable.where(cursor_column < after)
        elif after_with:
            selectable = selectable.where(cursor_column <= after_with)
    else:
        selectable = selectable.order_by(cursor_column)
        if before:
            selectable = selectable.where(cursor_column > before)
        elif before_with:
            selectable = selectable.where(cursor_column >= before_with)

    # Ordering
    if sort:
        order_col = get_column(selectable, sort)
        if not order == "asc":
            order_col = order_col.desc()
        selectable = selectable.order_by(order_col)
    return selectable
