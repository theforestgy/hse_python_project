# =============================================================================
# Модуль: Library/api_handler.py
#
# Описание:
# Этот модуль предоставляет функции для взаимодействия с API криптовалютных бирж
# с использованием библиотеки ccxt. Он инкапсулирует логику подключения
# к бирже, получения данных о ценах (тикеров) и обработки типичных ошибок API.
#
# =============================================================================

import ccxt
import pandas as pd
from datetime import datetime


def connect_to_exchange(exchange_name):
    """
    Создает и возвращает объект подключения к указанной бирже.

    Args:
        exchange_name (str): Имя биржи, поддерживаемое ccxt (например, 'binance').

    Returns:
        ccxt.Exchange: Объект биржи для дальнейшей работы.
        None: Если биржа не поддерживается или произошла ошибка инициализации.
    """
    try:
        exchange_class = getattr(ccxt, exchange_name)
        exchange = exchange_class({
            'enableRateLimit': True,  # Важно для соблюдения лимитов запросов API
        })
        print(f"Успешное подключение к бирже: {exchange_name}")
        return exchange
    except AttributeError:
        print(f"ОШИБКА: Биржа '{exchange_name}' не поддерживается библиотекой ccxt.")
        return None
    except Exception as e:
        print(f"ОШИБКА: Не удалось подключиться к бирже '{exchange_name}'. {e}")
        return None


def fetch_tickers(exchange, symbols):
    """
    Получает последние данные о ценах (тикеры) для списка криптовалютных пар.

    Args:
        exchange (ccxt.Exchange): Активный объект подключения к бирже.
        symbols (list): Список строковых символов (например, ['BTC/USDT', 'ETH/USDT']).

    Returns:
        pandas.DataFrame: DataFrame с данными о тикерах, содержащий столбцы
                          ['timestamp', 'symbol', 'price'].
                          Возвращает пустой DataFrame, если данные не удалось получить.
    """
    if not exchange or not symbols:
        return pd.DataFrame(columns=['timestamp', 'symbol', 'price'])

    try:
        # ccxt.fetch_tickers может принимать список символов для оптимизации
        tickers_data = exchange.fetch_tickers(symbols)

        # Если биржа вернула данные в нужном формате, преобразуем их
        if tickers_data:
            processed_data = []
            for symbol, ticker in tickers_data.items():
                if 'last' in ticker and ticker['last'] is not None:
                    # 'last' - это обычно последняя цена сделки
                    price = float(ticker['last'])
                    timestamp = datetime.now()  # Используем текущее время для единообразия
                    processed_data.append([timestamp, symbol, price])

            if processed_data:
                df = pd.DataFrame(processed_data, columns=['timestamp', 'symbol', 'price'])
                return df

        # Если предыдущий метод не сработал, попробуем по одному
        print("Предупреждение: пакетный запрос не удался, пробуем запросить тикеры по одному.")
        return fetch_tickers_safely(exchange, symbols)

    except (ccxt.NetworkError, ccxt.ExchangeError) as e:
        print(f"ОШИБКА API: Не удалось получить данные. {e}")
        return pd.DataFrame(columns=['timestamp', 'symbol', 'price'])
    except Exception as e:
        print(f"ОШИБКА: Произошла непредвиденная ошибка при получении тикеров. {e}")
        return pd.DataFrame(columns=['timestamp', 'symbol', 'price'])


def fetch_tickers_safely(exchange, symbols):
    """
    Безопасный метод получения тикеров по одному. Используется как запасной.
    """
    processed_data = []
    for symbol in symbols:
        try:
            ticker = exchange.fetch_ticker(symbol)
            if ticker and 'last' in ticker and ticker['last'] is not None:
                price = float(ticker['last'])
                timestamp = datetime.now()
                processed_data.append([timestamp, symbol, price])
        except (ccxt.NetworkError, ccxt.ExchangeError) as e:
            print(f"ОШИБКА API: Не удалось получить данные для {symbol}. {e}")
            continue  # Пропускаем этот символ и переходим к следующему

    if processed_data:
        df = pd.DataFrame(processed_data, columns=['timestamp', 'symbol', 'price'])
        return df
    else:
        return pd.DataFrame(columns=['timestamp', 'symbol', 'price'])


# --- Пример использования (для тестирования модуля) ---
if __name__ == '__main__':
    print("--- Тестирование модуля api_handler.py ---")

    # Параметры для теста
    test_exchange_name = 'binance'  # Можно поменять на другую биржу
    test_symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'INVALID/SYMBOL']

    exchange_instance = connect_to_exchange(test_exchange_name)

    if exchange_instance:
        print(f"\nЗапрашиваем данные для: {test_symbols}")
        tickers_df = fetch_tickers(exchange_instance, test_symbols)

        if not tickers_df.empty:
            print("\nУспешно получены данные:")
            print(tickers_df)
        else:
            print("\nНе удалось получить данные для указанных символов.")
