"""
"""
from __future__ import annotations

from functools import reduce
from typing import List, Dict


def change_camel_case_to_snake(camel_case: str):
    return reduce(
        lambda x, y: x + ("_" if y.isupper() else "") + y, camel_case
    ).lower()


def get_column(query, name):
    try:
        snake = change_camel_case_to_snake(name)
        return query.c[snake]
    except KeyError:
        raise KeyError("column {} not found".format(name))


def as_dict(resouce: list, columns: List[str]) -> List:
    results = []
    for row in resouce:
        summary = dict(zip(columns, row))
        results.append(summary)
    return results


def parse_filter_value(value: Dict[str, str]) -> List[Dict[str, str]]:
    filters = []
    for key, val in value.items():
        key_op = key.rsplit(".")
        if len(key_op) == 2:
            name, op = key_op
        else:
            raise ValueError(f"invalid key: {key}")
        filters.append({"name": name, "operation": op, "value": val})
    return filters