# =============================================================================
# Модуль: Library/data_analyzer.py
#
# Описание:
# Этот модуль содержит функции для анализа временных рядов данных о ценах.
# Основная функция - выявление аномалий на основе метода скользящего среднего
# и стандартного отклонения. Модуль работает с pandas DataFrame.
#
# =============================================================================

import pandas as pd
import numpy as np


def find_anomalies(history_df, current_price, symbol, window, threshold):
    """
    Анализирует историю цен и определяет, является ли текущая цена аномальной.

    Для каждого символа рассчитывается скользящее среднее и стандартное отклонение.
    Аномалией считается цена, выходящая за пределы:
    [скользящее среднее - threshold * ст. отклонение, скользящее среднее + threshold * ст. отклонение].

    Args:
        history_df (pd.DataFrame): DataFrame с историей цен. Должен содержать
                                   колонки 'symbol' и 'price'.
        current_price (float): Текущая цена для проверки.
        symbol (str): Символ криптовалютной пары (например, 'BTC/USDT').
        window (int): Размер окна для расчета скользящего среднего.
        threshold (float): Пороговый множитель для стандартного отклонения.

    Returns:
        dict or None: Возвращает словарь с информацией об аномалии, если она найдена.
                      Словарь содержит ключи: 'symbol', 'price', 'mean', 'threshold_value'.
                      Возвращает None, если аномалия не обнаружена или данных недостаточно.
    """
    # Фильтруем историю только для нужного символа
    symbol_history = history_df[history_df['symbol'] == symbol]['price']

    # Проверяем, достаточно ли данных для расчета
    if len(symbol_history) < window:
        # Недостаточно данных для формирования полного окна, аномалию определить нельзя
        return None

    # Берем последние `window` точек из истории для расчета статистики
    relevant_history = symbol_history.tail(window)

    # Рассчитываем скользящее среднее и стандартное отклонение по последним 'window' точкам
    rolling_mean = relevant_history.mean()
    rolling_std = relevant_history.std()

    # Проверяем, что статистика ВАЛИДНА (не NaN и не 0)
    if pd.isna(rolling_mean) or pd.isna(rolling_std) or rolling_std == 0:
        # std=0 означает, что все цены в истории были одинаковы.
        # Любое отклонение от них - аномалия.
        if rolling_std == 0 and current_price != rolling_mean:
             # Все цены были X, а новая Y. Это 100% аномалия.
             pass
        else:
             return None

    # Рассчитываем верхнюю и нижнюю границы нормы
    upper_bound = rolling_mean + (rolling_std * threshold)
    lower_bound = rolling_mean - (rolling_std * threshold)

    # Проверяем, является ли текущая цена аномальной
    if not (lower_bound <= current_price <= upper_bound):
        anomaly_info = {
            'symbol': symbol,
            'price': current_price,
            'mean': round(rolling_mean, 4),
            'deviation': round(abs(current_price - rolling_mean), 4),
            'upper_bound': round(upper_bound, 4),
            'lower_bound': round(lower_bound, 4)
        }
        return anomaly_info

    return None


# --- Пример использования (для тестирования модуля) ---
if __name__ == '__main__':
    print("--- Тестирование модуля data_analyzer.py (финальная, корректная версия) ---")

    # --- Параметры анализа ---
    test_window = 5
    test_threshold = 2.0
    print(f"\nПараметры анализа: окно = {test_window}, порог = {test_threshold}")

    # --- Создание тестовых данных ---
    # История из 5 одинаковых цен. Идеально для предсказуемых тестов.
    test_history = pd.DataFrame({
        'symbol': ['TEST/USD'] * test_window,
        'price': [100.0] * test_window
    })
    # На этой истории: mean = 100, std = 0.

    # --- Тест 1: Явная аномалия (на фоне нулевого отклонения) ---
    print("\n--- Тест 1: Явная аномалия ---")
    # История: [100, 100, 100, 100, 100]. Новая цена: 101.
    # mean=100, std=0. Границы: [100, 100]. 101 выходит за пределы.
    price_high = 101.0
    anomaly = find_anomalies(test_history, price_high, 'TEST/USD', test_window, test_threshold)
    if anomaly:
        print(f"УСПЕХ: Найдена аномалия: {anomaly}")
    else:
        print(f"ОШИБКА ТЕСТА: Аномалия для цены {price_high} не найдена.")

    # --- Тест 2: Нормальная цена ---
    print("\n--- Тест 2: Нормальная цена ---")
    # Создадим историю с небольшими колебаниями
    history_with_noise = pd.DataFrame({
        'symbol': ['TEST/USD'] * test_window,
        'price': [100, 102, 99, 101, 103]
    })
    # mean=101, std≈1.58. Границы: [101 - 2*1.58, 101 + 2*1.58] = [97.84, 104.16]
    # Новая цена 104 находится внутри коридора.
    price_norm = 104.0
    anomaly = find_anomalies(history_with_noise, price_norm, 'TEST/USD', test_window, test_threshold)
    if not anomaly:
        print("УСПЕХ: Нормальная цена не вызвала срабатывания.")
    else:
        print(f"ОШИБКА ТЕСТА: Найдена ложная аномалия {anomaly}.")

    # --- Тест 3: Аномалия (на фоне с колебаниями) ---
    print("\n--- Тест 3: Аномалия на фоне шума ---")
    # Используем ту же историю с колебаниями. mean=101, std≈1.58, UB≈104.16
    # Новая цена 105 выходит за верхнюю границу.
    price_high_noise = 105.0
    anomaly = find_anomalies(history_with_noise, price_high_noise, 'TEST/USD', test_window, test_threshold)
    if anomaly:
        print(f"УСПЕХ: Найдена аномалия: {anomaly}")
    else:
        print(f"ОШИБКА ТЕСТА: Аномалия для цены {price_high_noise} не найдена.")

    # --- Тест 4: Недостаточно данных ---
    print("\n--- Тест 4: Недостаточно данных ---")
    # История из 4 точек (меньше, чем test_window=5)
    history_small = test_history.head(test_window - 1)
    anomaly = find_anomalies(history_small, 150, 'TEST/USD', test_window, test_threshold)
    if not anomaly:
        print(f"УСПЕХ: Аномалия не определена, так как данных ({test_window - 1}) < окна ({test_window}).")
    else:
        print(f"ОШИБКА ТЕСТА: Найдена аномалия при недостаточном количестве данных.")
