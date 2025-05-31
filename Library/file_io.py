"""
Модуль file_io.py
Содержит базовые функции для чтения/записи справочников и отчётов.
"""

import os
import pickle

def read_binary_dict(file_path: str) -> dict:
    """
    Читает бинарный справочник из файла.
    :param file_path: путь к бинарному файлу
    :return: словарь с данными
    """
    # … (реализация)
    pass

def write_binary_dict(data: dict, file_path: str) -> None:
    """
    Сохраняет словарь в бинарный файл.
    :param data: словарь для сохранения
    :param file_path: путь для сохранения бинарного файла
    """
    # … (реализация)
    pass

def save_text_report(text: str, file_path: str) -> None:
    """
    Сохраняет текстовый отчёт в файл.
    :param text: содержимое отчёта
    :param file_path: путь к файлу (Output/)
    """
    # … (реализация)
    pass

def save_figure(fig, file_path: str) -> None:
    """
    Сохраняет объект matplotlib.figure в файл.
    :param fig: объекты типа matplotlib.figure.Figure
    :param file_path: полный путь (Graphics/)
    """
    # … (реализация)
    pass
