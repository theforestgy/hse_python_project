"""
Модуль db_utils.py
Универсальные функции для работы с базой данных (построенной на основе справочников).
"""

import sqlite3
from typing import List, Tuple, Any

def connect_db(db_path: str) -> sqlite3.Connection:
    """
    Подключается к SQLite-файлу (или создаёт новый).
    :param db_path: путь к файлу БД (внутри Data/ или отдельный)
    :return: объект sqlite3.Connection
    """
    # … (реализация)
    pass

def create_tables(conn: sqlite3.Connection) -> None:
    """
    Создаёт все необходимые таблицы (если их нет) на основе справочников.
    The schema должна соответствовать 3-НФ.
    :param conn: sqlite3.Connection
    """
    # … (реализация)
    pass

def load_reference_tables(conn: sqlite3.Connection, data_dir: str) -> None:
    """
    «Заполняет» таблицы-справочники из бинарных файлов (Data/*.bin) при старте.
    :param conn: sqlite3.Connection
    :param data_dir: путь к каталогу Data/
    """
    # … (реализация)
    pass

def insert_dynamic_record(conn: sqlite3.Connection, table: str, record: Tuple) -> None:
    """
    Вставляет новую запись в указанную таблицу.
    :param conn: sqlite3.Connection
    :param table: название таблицы
    :param record: кортеж с данными
    """
    # … (реализация)
    pass

def query_table(conn: sqlite3.Connection, query: str, params: Tuple = ()) -> List[Tuple]:
    """
    Делает общий SELECT-запрос к БД с подстановкой параметров.
    :param conn: sqlite3.Connection
    :param query: текст SQL-запроса
    :param params: кортеж параметров (по умолчанию пустой)
    :return: список кортежей с результатами
    """
    # … (реализация)
    pass
