"""
data_collection.py
Модуль для сбора данных с API бирж (Binance, Coinbase и т.д.).
"""

import time
import requests  # или aiohttp, если используем asyncio
from typing import Dict, Any, List
from Library.utils import get_current_timestamp

def fetch_binance_price(symbol: str, api_key: str, secret: str) -> Dict[str, Any]:
    """
    Запрашивает текущую цену symbol у Binance.
    :param symbol: строка (например, "BTCUSDT")
    :param api_key: ключ API
    :param secret: секретный ключ
    :return: словарь с ценой и timestamp
    """
    # … (реализация)
    pass

def fetch_coinbase_price(symbol: str, api_key: str, secret: str) -> Dict[str, Any]:
    """
    Запрашивает текущую цену symbol у Coinbase.
    :param symbol: строка (например, "BTC-USD")
    :param api_key: ключ API
    :param secret: секрет
    :return: словарь с ценой и timestamp
    """
    # … (реализация)
    pass

def fetch_all_prices_once(symbols: List[str], exchange_configs: Dict[str, Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Функция, которая разово получает цены для списка символов.
    :param symbols: ["BTC", "ETH", ...]
    :param exchange_configs: {"binance": {"api_key": "...", "secret": "..."}, "coinbase": {...}}
    :return: список словарей вида {"exchange": "binance", "symbol": "BTC", "price": 50000.0, "timestamp": "2025-05-31 10:00:00"}
    """
    # … (реализация)
    pass

def fetch_all_prices_loop(interval: int, symbols: List[str], exchange_configs: Dict[str, Dict[str, str]], db_conn) -> None:
    """
    Бесконечный (или пока приложение запущено) цикл опроса цен с заданным интервалом.
    После получения данных вызывает функцию сохранения в БД.
    :param interval: задержка между запросами (секунды)
    :param symbols: список символов
    :param exchange_configs: словарь конфига для бирж
    :param db_conn: соединение с БД
    """
    while True:
        # 1) fetch_all_prices_once(...)
        # 2) сохраняем в БД через db_manager.insert_price_record(...)
        time.sleep(interval)
