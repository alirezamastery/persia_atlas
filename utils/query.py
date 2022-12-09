from typing import Union

from django.db import connection


def execute_raw_query(sql: str, params: Union[list, dict, tuple]) -> list[tuple]:
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()


def raw_query_auto_named(sql: str, params: Union[list, dict, tuple]) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


__all__ = [
    'execute_raw_query',
    'raw_query_auto_named',
]
