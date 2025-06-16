# =============================================================================
# Модуль: Scripts/main.py
#
# Описание:
# Главный исполняемый файл приложения.
# Отвечает за инициализацию, запуск основного цикла приложения,
# координацию работы всех модулей (config, api, analysis, ui).
#
# =============================================================================

import os
import sys
import pandas as pd
from datetime import datetime
from tkinter import filedialog, messagebox, NORMAL

# --- Добавляем путь к корневой директории проекта, чтобы импорты работали ---
# Это позволяет запускать main.py напрямую из папки Scripts
# и корректно находить модули в Library
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# --- Импорты из нашего проекта ---
import Scripts.config_manager as cm
import Scripts.ui_manager as ui
import Library.api_handler as api
import Library.data_analyzer as analyzer

# --- Глобальные переменные для хранения состояния ---
# Используем словарь для группировки, чтобы не плодить много глобальных переменных
app_state = {
    'config': None,
    'exchange': None,
    'root': None,
    'widgets': None,
    'history_df': pd.DataFrame(columns=['timestamp', 'symbol', 'price']),
    'selected_symbol_for_graph': None
}


def load_log_file(log_path):
    """Загружает существующий лог аномалий, если он есть."""
    if os.path.exists(log_path):
        try:
            log_df = pd.read_csv(log_path)
            # Заполняем лог в интерфейсе в обратном порядке для правильного отображения
            for index, row in log_df.iloc[::-1].iterrows():
                anomaly_info = {
                    'symbol': row['symbol'],
                    'price': row['price'],
                    'lower_bound': row['lower_bound'],
                    'upper_bound': row['upper_bound']
                }
                # Времени у нас нет, но остальные данные есть
                desc = f"Цена вышла за пределы нормы ({anomaly_info['lower_bound']} - {anomaly_info['upper_bound']})"
                values = (row['timestamp'], row['symbol'], f"{row['price']:.4f}", desc)
                app_state['widgets']['anomaly_tree'].insert("", 0, values=values)
        except Exception as e:
            print(f"Ошибка при загрузке лог-файла {log_path}: {e}")


def save_anomaly_to_log(anomaly_info, log_path):
    """Сохраняет информацию об аномалии в CSV файл."""
    try:
        header = not os.path.exists(log_path)
        log_entry = pd.DataFrame([{
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'symbol': anomaly_info['symbol'],
            'price': anomaly_info['price'],
            'mean': anomaly_info['mean'],
            'deviation': anomaly_info['deviation'],
            'lower_bound': anomaly_info['lower_bound'],
            'upper_bound': anomaly_info['upper_bound']
        }])
        log_entry.to_csv(log_path, mode='a', header=header, index=False)
    except Exception as e:
        print(f"Ошибка при записи в лог-файл {log_path}: {e}")


def save_graph_to_file():
    """
    Обработчик нажатия на кнопку сохранения графика.
    Сохраняет текущий график в файл изображения.
    """
    figure_to_save = app_state['widgets']['graph_figure']
    selected_symbol = app_state.get('selected_symbol_for_graph', 'chart')

    # Если по какой-то причине символ не выбран, ничего не делаем
    if not selected_symbol:
        messagebox.showwarning("Сохранение", "Сначала выберите символ в таблице.")
        return

    try:
        # Формируем имя файла: SYMBOL_YYYYMMDD_HHMMSS.png
        filename = f"{selected_symbol.replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        graphics_dir = '../Graphics'
        filepath = os.path.join(graphics_dir, filename)

        # Сохраняем файл
        figure_to_save.savefig(filepath, dpi=300, bbox_inches='tight')

        # Сообщаем пользователю об успехе
        messagebox.showinfo("Сохранение графика", f"График успешно сохранен:\n{os.path.abspath(filepath)}")

    except Exception as e:
        messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить график.\nОшибка: {e}")


def main_update_cycle():
    """
    Основной цикл обновления данных и интерфейса.
    Вызывается периодически с помощью root.after().
    """
    config = app_state['config']
    exchange = app_state['exchange']
    widgets = app_state['widgets']

    # 1. Получаем свежие данные с биржи
    print("Обновление данных...")
    current_data_df = api.fetch_tickers(exchange, config['api']['symbols'])

    if current_data_df.empty:
        print("Не удалось получить свежие данные. Пропускаем цикл.")
        widgets['status_label'].config(text="Ошибка обновления! Проверьте интернет или API биржи.")
    else:
        # 2. Обновляем историю
        app_state['history_df'] = pd.concat([app_state['history_df'], current_data_df], ignore_index=True)
        # Ограничиваем размер истории, чтобы не съедать всю память
        max_history_size = len(config['api']['symbols']) * 1000
        if len(app_state['history_df']) > max_history_size:
            app_state['history_df'] = app_state['history_df'].tail(max_history_size)

        # 3. Анализируем данные на аномалии
        found_anomalies = []
        for index, row in current_data_df.iterrows():
            anomaly = analyzer.find_anomalies(
                history_df=app_state['history_df'],
                current_price=row['price'],
                symbol=row['symbol'],
                window=config['analysis']['moving_average_window'],
                threshold=config['analysis']['standard_deviation_threshold']
            )
            if anomaly:
                found_anomalies.append(anomaly)
                # 4. Обновляем лог в UI и в файле
                ui.update_anomaly_log(widgets['anomaly_tree'], anomaly)
                save_anomaly_to_log(anomaly, config['logging']['log_file'])

        # 5. Обновляем интерфейс
        ui.update_prices_table(widgets['prices_tree'], current_data_df, found_anomalies, config)
        ui.update_status_bar(widgets['status_label'], datetime.now())

        # Обновляем график, если выбран какой-то символ
        if app_state['selected_symbol_for_graph']:
            ui.update_graph(
                widgets['graph_ax'], widgets['graph_canvas'],
                app_state['history_df'], app_state['selected_symbol_for_graph'],
                config
            )

    # 6. Планируем следующий запуск этого же цикла
    update_interval_ms = config['analysis']['update_interval_seconds'] * 1000
    app_state['root'].after(update_interval_ms, main_update_cycle)


def on_symbol_select(event):
    """Обработчик события выбора строки в таблице цен."""
    widget = event.widget
    if not widget.selection():
        return

    selected_item = widget.selection()[0]
    selected_symbol = widget.item(selected_item, 'values')[0]
    app_state['selected_symbol_for_graph'] = selected_symbol

    # Сразу обновляем график
    ui.update_graph(
        app_state['widgets']['graph_ax'], app_state['widgets']['graph_canvas'],
        app_state['history_df'], selected_symbol, app_state['config']
    )

    app_state['widgets']['save_graph_button'].config(state=NORMAL)


def main():
    """Главная функция, точка входа в приложение."""
    try:
        # 1. Загружаем конфигурацию
        config_path = os.path.join(project_root, 'config.ini')
        config = cm.load_config(config_path)
        app_state['config'] = config

        # 2. Подключаемся к бирже
        exchange = api.connect_to_exchange(config['api']['exchange'])
        if not exchange:
            print("Не удалось подключиться к бирже. Приложение будет закрыто.")
            return
        app_state['exchange'] = exchange

        # 3. Создаем GUI
        root = ui.create_main_window(config)
        app_state['root'] = root

        ui.create_styles(config)
        frames = ui.create_frames(root, config)
        widgets = ui.create_widgets(frames, config)
        app_state['widgets'] = widgets

        # Привязываем обработчики
        widgets['prices_tree'].bind('<<TreeviewSelect>>', on_symbol_select)
        # Обработчик для кнопки Сохранить в файл
        widgets['save_graph_button'].config(command=save_graph_to_file)

        # Загружаем старые аномалии из лога
        load_log_file(config['logging']['log_file'])

        # 4. Запускаем первый цикл обновления и затем главный цикл Tkinter
        print("Запуск приложения...")
        root.after(1000, main_update_cycle)  # Запускаем первый апдейт через 1 секунду
        root.mainloop()

    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА при инициализации: {e}")
        input("Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()
