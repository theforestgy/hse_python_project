# =============================================================================
# Модуль: Scripts/config_manager.py
#
# Описание:
# Этот модуль отвечает за чтение и обработку конфигурационного файла config.ini.
# Он использует стандартную библиотеку configparser для парсинга .ini файла
# и предоставляет загруженные настройки в виде структурированного словаря.
#
# =============================================================================

import configparser
import os

# --- КОНСТАНТЫ ---
CONFIG_FILE_PATH = 'config.ini'


def load_config(path=CONFIG_FILE_PATH):
    """
    Загружает и парсит конфигурационный файл.

    Читает файл config.ini, расположенный в корневой директории проекта.
    Преобразует строковые значения в нужные типы данных (числа, списки).
    В случае отсутствия файла или секции вызывает исключение.

    Args:
        path (str): Путь к файлу конфигурации. По умолчанию 'config.ini'.

    Returns:
        dict: Словарь с конфигурационными параметрами, сгруппированными по секциям.

    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
        KeyError: Если обязательная секция или параметр отсутствует в файле.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл конфигурации не найден по пути: {path}")

    config = configparser.ConfigParser()
    config.read(path, encoding='utf-8')

    settings = {}

    try:
        # --- Секция API ---
        settings['api'] = {
            'exchange': config.get('API', 'exchange'),
            'symbols': [s.strip() for s in config.get('API', 'symbols').split(',')]
        }

        # --- Секция Analysis ---
        settings['analysis'] = {
            'update_interval_seconds': config.getint('Analysis', 'update_interval_seconds'),
            'moving_average_window': config.getint('Analysis', 'moving_average_window'),
            'standard_deviation_threshold': config.getfloat('Analysis', 'standard_deviation_threshold')
        }

        # --- Секция UI ---
        settings['ui'] = {
            'theme': config.get('UI', 'theme'),
            'font_family': config.get('UI', 'font_family'),
            'font_size': config.getint('UI', 'font_size'),
            'background_color': config.get('UI', 'background_color'),
            'text_color': config.get('UI', 'text_color'),
            'success_color': config.get('UI', 'success_color'),
            'anomaly_color': config.get('UI', 'anomaly_color'),
            'graph_line_color': config.get('UI', 'graph_line_color')
        }

        # --- Секция Logging ---
        settings['logging'] = {
            'log_file': config.get('Logging', 'log_file')
        }

    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        raise KeyError(f"Ошибка в файле конфигурации: отсутствует обязательный параметр или секция. {e}")

    # Проверка на наличие хотя бы одной отслеживаемой криптовалюты
    if not settings['api']['symbols']:
        raise ValueError(
            "В файле конфигурации (секция API, параметр 'symbols') должен быть указан хотя бы один символ для отслеживания.")

    return settings


# --- Пример использования (для тестирования модуля) ---
if __name__ == '__main__':
    print("--- Тестирование модуля config_manager.py ---")
    try:
        # Предполагается, что вы запускаете этот скрипт из папки Scripts,
        # поэтому для теста нужно подняться на уровень выше к config.ini
        project_root_config_path = os.path.join(os.path.dirname(__file__), '..', CONFIG_FILE_PATH)

        loaded_settings = load_config(project_root_config_path)

        print("Конфигурация успешно загружена:")
        import json

        print(json.dumps(loaded_settings, indent=4))

        print("\nПроверка доступа к параметрам:")
        print(f"Биржа: {loaded_settings['api']['exchange']}")
        print(f"Список символов: {loaded_settings['api']['symbols']}")
        print(f"Интервал обновления: {loaded_settings['analysis']['update_interval_seconds']} сек.")

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"ОШИБКА: {e}")
