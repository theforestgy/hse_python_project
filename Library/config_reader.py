"""
Модуль config_reader.py
Отвечает за чтение параметров из config.ini.
"""

import configparser
from typing import Dict, Any

def load_config(config_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Загружает конфигурации из .ini-файла.
    :param config_path: путь к файлу config.ini
    :return: вложенный словарь {section: {key: value}}
    """
    # … (реализация)
    pass

def get_section(config: Dict[str, Dict[str, Any]], section: str) -> Dict[str, Any]:
    """
    Возвращает параметры указанного раздела.
    :param config: результат load_config
    :param section: название секции в ini (например, "API", "UI")
    :return: словарь ключей и значений для этой секции
    """
    # … (реализация)
    pass
