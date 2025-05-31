"""
report_generator.py
Модуль для формирования информационно-аналитических отчётов (текстовых и графических).
Использует pandas и matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Tuple, Any

def generate_projection_report(db_conn, columns: List[str], filters: dict) -> pd.DataFrame:
    """
    Простой текстовый отчёт за счёт операций проекции и сокращения (pandas).
    :param db_conn: sqlite3.Connection
    :param columns: список столбцов для отображения
    :param filters: словарь вида {"column": value, ...} для фильтрации строк
    :return: DataFrame с результатом
    """
    # … (реализация, использует pandas.read_sql_query + DataFrame.drop)
    pass

def generate_statistical_report(db_conn, qualitative_cols: List[str], quantitative_cols: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Текстовый статистический отчёт:
    - Таблица частот для качественных переменных
    - Описательные статистики для количественных переменных
    :param db_conn: sqlite3.Connection
    :param qualitative_cols: список строковых (качественных) колонок
    :param quantitative_cols: список числовых колонок
    :return: кортеж (freq_table: DataFrame, stats_table: DataFrame)
    """
    # … (реализация через pandas)
    pass

def generate_pivot_table_report(db_conn, index: str, columns: str, values: str, aggfunc: str) -> pd.DataFrame:
    """
    Текстовый отчёт «сводная таблица» для пары качественных атрибутов.
    :param db_conn: sqlite3.Connection
    :param index: колонка-индекс
    :param columns: колонка-столбец
    :param values: колонка-значение
    :param aggfunc: функция агрегации ("sum", "mean", "count" и т.п.)
    :return: DataFrame (pivot_table)
    """
    # … (реализация через pandas.pivot_table)
    pass

def generate_bar_chart_report(db_conn, cat_col1: str, cat_col2: str, output_path: str) -> None:
    """
    Графический отчёт: «кластеризованная столбчатая диаграмма» для (категория-категория).
    Использует matplotlib.pyplot.bar().
    :param db_conn: sqlite3.Connection
    :param cat_col1: первая категориальная колонка
    :param cat_col2: вторая категориальная колонка
    :param output_path: куда сохранить картинку (в Graphics/)
    """
    # … (реализация)
    pass

def generate_histogram_report(db_conn, num_col: str, cat_col: str, output_path: str) -> None:
    """
    Графический отчёт: «категоризированная гистограмма» для (количественная-категория).
    Использует matplotlib.pyplot.hist().
    """
    # … (реализация)
    pass

def generate_boxplot_report(db_conn, num_col: str, cat_col: str, output_path: str) -> None:
    """
    Графический отчёт: «категоризированная диаграмма Бокса-Вискера» для (количественная-категория).
    Использует matplotlib.pyplot.boxplot().
    """
    # … (реализация)
    pass

def generate_scatter_report(db_conn, num_col_x: str, num_col_y: str, cat_col: str, output_path: str) -> None:
    """
    Графический отчёт: «категоризированная диаграмма рассеивания» (2 количественные + 1 категориальная).
    Использует matplotlib.pyplot.scatter().
    """
    # … (реализация)
    pass
