from typing import Union

from django.db import connection


def execute_raw_query(sql: str, params: Union[list, dict, tuple]) -> list[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


__all__ = [
    'execute_raw_query'
]
