"""
gui.py
Модуль для построения графического интерфейса на базе Tk (Tkinter).
Весь интерфейс — на русском языке, без «специальной» терминологии.
"""

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable, List

def launch_gui(config: dict, db_conn: Any) -> None:
    """
    Создаёт окно Tk, настраивает все вкладки/фреймы:
    1) Вкладка настроек API (ввод ключей, выбор биржи)
    2) Вкладка выбора криптовалют для отслеживания
    3) Вкладка настроек анализа (окно MA, порог) и оповещений
    4) Вкладка просмотра текущих котировок + истории аномалий (таблица)
    5) Вкладка визуализации (графики цен с выделением аномалий)
    """
    root = tk.Tk()
    root.title("Мониторинг аномалий криптовалют")
    # Устанавливаем размеры, цвета, шрифты из config['UI']

    # --- Настройка вкладок через ttk.Notebook ---
    notebook = ttk.Notebook(root)
    frame_api = ttk.Frame(notebook)
    frame_symbols = ttk.Frame(notebook)
    frame_analysis = ttk.Frame(notebook)
    frame_alerts = ttk.Frame(notebook)
    frame_visualization = ttk.Frame(notebook)

    notebook.add(frame_api, text="Настройки API")
    notebook.add(frame_symbols, text="Выбор криптовалют")
    notebook.add(frame_analysis, text="Параметры анализа")
    notebook.add(frame_alerts, text="История аномалий")
    notebook.add(frame_visualization, text="Визуализация")
    notebook.pack(fill='both', expand=True)

    # TODO: внутри каждого frame_* вызываем функции-строители интерфейса
    # Например: build_api_frame(frame_api, config, db_conn)
    #           build_symbols_frame(frame_symbols, config, db_conn)
    # и т.д.

    root.mainloop()

def build_api_frame(parent: tk.Frame, config: dict, db_conn: Any) -> None:
    """
    Строит форму для ввода/сохранения API-ключей и выбора биржи.
    :param parent: родительский фрейм
    :param config: словарь конфигурации
    :param db_conn: соединение с БД (для сохранения изменений)
    """
    # … (реализация формы)
    pass

def build_symbols_frame(parent: tk.Frame, config: dict, db_conn: Any) -> None:
    """
    Строит форму для выбора списка криптовалют (минимум 5).
    :param parent: родительский фрейм
    :param config: словарь конфигурации
    :param db_conn: соединение с БД
    """
    # … (реализация)
    pass

def build_analysis_frame(parent: tk.Frame, config: dict, db_conn: Any) -> None:
    """
    Строит форму для ввода параметров анализа (окно MA, порог, частоту).
    """
    # … (реализация)
    pass

def build_alerts_frame(parent: tk.Frame, config: dict, db_conn: Any) -> None:
    """
    Строит таблицу текущих котировок и историю аномалий (с возможностью фильтрации).
    """
    # … (реализация)
    pass

def build_visualization_frame(parent: tk.Frame, config: dict, db_conn: Any) -> None:
    """
    Строит области для отображения графиков:
    - Реальное время: график цен с пометками найденных аномалий
    - Исторические графики (выбор периода)
    """
    # … (реализация)
    pass
