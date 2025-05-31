"""
Модуль utils.py
Содержит различные вспомогательные функции, не относящиеся к конкретным подсистемам.
"""

import datetime
from typing import List, Dict, Any

def get_current_timestamp() -> str:
    """
    Возвращает текущую дату и время в виде строки (ISO-формат).
    :return: строка 'YYYY-MM-DD HH:MM:SS'
    """
    # … (реализация)
    pass

def moving_average(data: List[float], window: int) -> List[float]:
    """
    Вычисляет скользящее среднее по списку чисел.
    :param data: список цен (float)
    :param window: размер окна
    :return: список скользящих средних
    """
    # … (реализация)
    pass

def detect_anomalies(prices: List[float], ma: List[float], threshold: float) -> List[int]:
    """
    Находит индексы аномалий: когда |price_i - ma_i| > threshold
    :param prices: исторические цены
    :param ma: скользящее среднее
    :param threshold: порог (например, в процентах или в абсолютных единицах)
    :return: список индексов (или временных меток) аномалий
    """
    # … (реализация)
    pass
