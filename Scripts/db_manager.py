"""
db_manager.py
Модуль для операций над «операционными» таблицами БД: добавление новых записей (цен, аномалий), модификация справочников, ручное добавление/удаление элементов.
"""

import sqlite3
from typing import Dict, Any

def insert_price_record(db_conn: sqlite3.Connection, symbol: str, exchange: str, price: float, timestamp: str) -> None:
    """
    Добавляет запись о текущей цене в таблицу prices.
    :param db_conn: sqlite3.Connection
    :param symbol: "BTC", "ETH" и т.д.
    :param exchange: из какого источника (binance, coinbase)
    :param price: текущая цена
    :param timestamp: строка с датой/временем
    """
    # … (реализация)
    pass

def insert_anomaly_record(db_conn: sqlite3.Connection, symbol: str, timestamp: str, price: float, ma: float, diff: float) -> None:
    """
    Добавляет запись о найденной аномалии в таблицу anomalies.
    :param db_conn: sqlite3.Connection
    :param symbol: криптовалюта
    :param timestamp: время
    :param price: текущая цена
    :param ma: значение скользящего среднего
    :param diff: разница
    """
    # … (реализация)
    pass

def manual_add_reference(db_conn: sqlite3.Connection, table: str, fields: Dict[str, Any]) -> None:
    """
    Ручное добавление новой сущности в справочник (через GUI).
    :param db_conn: sqlite3.Connection
    :param table: имя таблицы-справочника (например, 'currencies', 'exchanges')
    :param fields: словарь {"column1": value1, "column2": value2, ...}
    """
    # … (реализация)
    pass

def manual_delete_reference(db_conn: sqlite3.Connection, table: str, record_id: int) -> None:
    """
    Ручное удаление записи-справочника по её ID.
    """
    # … (реализация)
    pass

def manual_update_reference(db_conn: sqlite3.Connection, table: str, record_id: int, fields: Dict[str, Any]) -> None:
    """
    Ручная модификация существующей записи в справочнике.
    """
    # … (реализация)
    pass
