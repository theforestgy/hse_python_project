"""
main.py
Главный скрипт приложения. Запускает GUI, инициализирует все подсистемы.
"""

import os
import sys
import tkinter as tk

from Library.config_reader import load_config, get_section
from Library.db_utils import connect_db, create_tables, load_reference_tables
from data_collection import fetch_all_prices_loop
from analysis import analyze_new_data_loop
from alerts import start_alerts_loop
from gui import launch_gui

def main():
    """
    Точка входа в приложение.
    Шаги:
    1. Загружаем конфиг из config.ini
    2. Подключаемся к БД и создаём таблицы (если нужно)
    3. Загружаем справочники из Data/
    4. Инициализируем потоки/задачи: сбор данных, анализ, оповещения
    5. Запускаем GUI (tkinter mainloop)
    """
    # 1. Загружаем конфигурацию
    config_path = os.path.join(os.getcwd(), 'config.ini')
    config = load_config(config_path)

    # 2. Настраиваем соединение с БД
    db_path = os.path.join(os.getcwd(), get_section(config, 'Paths')['data_dir'], 'crypto.db')
    conn = connect_db(db_path)
    create_tables(conn)
    load_reference_tables(conn, get_section(config, 'Paths')['data_dir'])

    # 3. Запуск фоновых задач
    # Здесь можно использовать threading или asyncio (в функциональном стиле)
    # … (запускаем fetch_all_prices_loop, analyze_new_data_loop, start_alerts_loop)

    # 4. Запуск графического интерфейса
    launch_gui(config, conn)

if __name__ == '__main__':
    main()
