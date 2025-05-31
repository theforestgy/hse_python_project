"""
alerts.py
Модуль для формирования и отправки оповещений пользователю (GUI-коллбэки).
"""

from typing import List, Dict, Any

def format_alert_message(anomaly: Dict[str, Any], symbol: str) -> str:
    """
    Форматирует строку оповещения на русском языке.
    Пример: «[12:05:30] ⚠️ Аномалия для BTC: цена 50000.0 отклонилась от MA (48000.0) на 2000.0»
    :param anomaly: словарь вида {"timestamp": ..., "price": ..., "ma": ..., "diff": ...}
    :param symbol: "BTC", "ETH" и т.д.
    :return: строковое сообщение
    """
    # … (реализация)
    pass

def start_alerts_loop(alert_queue, gui_callback) -> None:
    """
    Цикл, который читает из alert_queue и передаёт каждую аномалию в GUI (через gui_callback).
    :param alert_queue: очередь аномалий
    :param gui_callback: функция, которая отображает оповещение в интерфейсе
    """
    while True:
        # ждём новую аномалию; вызываем gui_callback(message)
        pass
