# =============================================================================
# Модуль: Scripts/ui_manager.py
#
# Описание:
# Отвечает за создание и управление графическим интерфейсом пользователя (GUI)
# на базе Tkinter. Создает главное окно, фреймы, виджеты (метки, таблицы,
# графики) и предоставляет функции для их обновления.
#
# =============================================================================

import tkinter as tk
from tkinter import ttk, font
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


# --- Функции для создания элементов GUI ---

def create_main_window(config):
    """Создает и настраивает главное окно приложения."""
    root = tk.Tk()
    root.title("Крипто-бот для отслеживания аномалий")
    root.geometry("900x800")
    root.configure(bg=config['ui']['background_color'])
    return root


def create_styles(config):
    """Создает и настраивает стили для виджетов ttk."""
    style = ttk.Style()
    style.theme_use('clam')  # Используем тему, которую легко настроить

    # Стиль для Treeview (таблицы)
    style.configure("Treeview",
                    background=config['ui']['background_color'],
                    foreground=config['ui']['text_color'],
                    fieldbackground=config['ui']['background_color'],
                    font=(config['ui']['font_family'], config['ui']['font_size']))
    style.map('Treeview', background=[('selected', config['ui']['success_color'])])

    # Стиль для заголовков Treeview
    style.configure("Treeview.Heading",
                    font=(config['ui']['font_family'], config['ui']['font_size'] + 1, 'bold'))

    # Стиль для обычных меток
    style.configure("TLabel",
                    background=config['ui']['background_color'],
                    foreground=config['ui']['text_color'],
                    font=(config['ui']['font_family'], config['ui']['font_size']))

    # Стиль для статус-бара
    style.configure("Status.TLabel",
                    font=(config['ui']['font_family'], config['ui']['font_size'] - 1))


def create_frames(root, config):
    """Создает и размещает основные фреймы (контейнеры) в главном окне."""
    frames = {}

    # Фрейм для основной таблицы с ценами
    frames['prices_frame'] = ttk.Frame(root, padding="10")
    frames['prices_frame'].pack(fill=tk.X, padx=10, pady=5)

    # Фрейм для графика
    frames['graph_frame'] = ttk.Frame(root, padding="10")
    frames['graph_frame'].pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Фрейм для лога аномалий
    frames['anomaly_frame'] = ttk.Frame(root, padding="10")
    frames['anomaly_frame'].pack(fill=tk.X, padx=10, pady=5)

    # Фрейм для статус-бара внизу
    frames['status_frame'] = ttk.Frame(root, padding="5")
    frames['status_frame'].pack(fill=tk.X, side=tk.BOTTOM, padx=10)

    return frames


def create_widgets(frames, config):
    """Создает все виджеты и размещает их в соответствующих фреймах."""
    widgets = {}

    # --- Виджеты для фрейма с ценами ---
    widgets['prices_label'] = ttk.Label(frames['prices_frame'], text="Текущие котировки",
                                        font=(config['ui']['font_family'], 12, 'bold'))
    widgets['prices_label'].pack(anchor=tk.W)

    cols = ('Символ', 'Цена', 'Статус')
    widgets['prices_tree'] = ttk.Treeview(frames['prices_frame'], columns=cols, show='headings', height=5)
    for col in cols:
        widgets['prices_tree'].heading(col, text=col)
    widgets['prices_tree'].column('Символ', width=150)
    widgets['prices_tree'].column('Цена', width=150, anchor=tk.E)
    widgets['prices_tree'].column('Статус', width=400, anchor=tk.W)
    widgets['prices_tree'].pack(fill=tk.X, pady=5)

    # --- Виджеты для фрейма с графиком ---
    graph_header_frame = ttk.Frame(frames['graph_frame'])
    graph_header_frame.pack(fill=tk.X, pady=(0, 5))

    widgets['graph_label'] = ttk.Label(graph_header_frame, text="История цен",
                                       font=(config['ui']['font_family'], 12, 'bold'))
    widgets['graph_label'].pack(side=tk.LEFT)

    widgets['save_graph_button'] = ttk.Button(graph_header_frame, text="Сохранить график")
    widgets['save_graph_button'].config(state=tk.DISABLED)
    widgets['save_graph_button'].pack(side=tk.RIGHT)

    fig = Figure(figsize=(5, 3), dpi=100, facecolor=config['ui']['background_color'])
    ax = fig.add_subplot(111)
    ax.set_facecolor(config['ui']['background_color'])
    ax.tick_params(axis='x', colors=config['ui']['text_color'])
    ax.tick_params(axis='y', colors=config['ui']['text_color'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(config['ui']['text_color'])
    ax.spines['bottom'].set_color(config['ui']['text_color'])

    widgets['graph_figure'] = fig
    widgets['graph_ax'] = ax
    widgets['graph_canvas'] = FigureCanvasTkAgg(fig, master=frames['graph_frame'])
    widgets['graph_canvas'].get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # --- Виджеты для лога аномалий ---
    widgets['anomaly_label'] = ttk.Label(frames['anomaly_frame'], text="Лог аномалий", font=(config['ui']['font_family'], 12, 'bold'))
    widgets['anomaly_label'].pack(anchor=tk.W) # Просто размещаем слева

    anomaly_cols = ('Время', 'Символ', 'Цена', 'Описание')
    widgets['anomaly_tree'] = ttk.Treeview(frames['anomaly_frame'], columns=anomaly_cols, show='headings', height=4)
    for col in anomaly_cols:
        widgets['anomaly_tree'].heading(col, text=col)
    widgets['anomaly_tree'].column('Время', width=150)
    widgets['anomaly_tree'].column('Символ', width=120)
    widgets['anomaly_tree'].column('Цена', width=120, anchor=tk.E)
    widgets['anomaly_tree'].column('Описание', width=410)
    widgets['anomaly_tree'].pack(fill=tk.X, pady=5)

    # --- Виджеты для статус-бара ---
    widgets['status_label'] = ttk.Label(frames['status_frame'], text="Инициализация...", style="Status.TLabel")
    widgets['status_label'].pack(side=tk.LEFT)

    return widgets


# --- Функции для обновления GUI ---

def update_prices_table(tree, data_df, anomalies, config):
    """Обновляет таблицу с текущими ценами, подсвечивая аномалии."""
    tree.delete(*tree.get_children())  # Очищаем старые записи

    anomaly_symbols = [a['symbol'] for a in anomalies]

    for index, row in data_df.iterrows():
        symbol = row['symbol']
        price = f"{row['price']:.4f}"

        if symbol in anomaly_symbols:
            status = "!!! АНОМАЛИЯ !!!"
            tag = 'anomaly'
        else:
            status = "В норме"
            tag = 'normal'

        tree.insert("", tk.END, values=(symbol, price, status), tags=(tag,))

    tree.tag_configure('anomaly', background=config['ui']['anomaly_color'], foreground='white')
    tree.tag_configure('normal', background=config['ui']['background_color'], foreground=config['ui']['text_color'])


def update_anomaly_log(tree, anomaly_info):
    """Добавляет новую запись об аномалии в таблицу лога."""
    desc = f"Цена вышла за пределы нормы ({anomaly_info['lower_bound']} - {anomaly_info['upper_bound']})"
    values = (
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        anomaly_info['symbol'],
        f"{anomaly_info['price']:.4f}",
        desc
    )
    tree.insert("", 0, values=values)  # Вставляем в начало


def update_graph(ax, canvas, history_df, selected_symbol, config):
    """Перерисовывает график для выбранного символа."""
    ax.clear()

    if selected_symbol and not history_df.empty:
        symbol_data = history_df[history_df['symbol'] == selected_symbol]
        if not symbol_data.empty:
            ax.plot(symbol_data['timestamp'], symbol_data['price'],
                    color=config['ui']['graph_line_color'], marker='.', linestyle='-')
            ax.set_title(f"История цен для {selected_symbol}", color=config['ui']['text_color'])
            ax.set_ylabel("Цена (USDT)", color=config['ui']['text_color'])
            # Автоформатирование дат на оси X
            fig = ax.get_figure()
            fig.autofmt_xdate()
    else:
        ax.set_title("Выберите символ в таблице для отображения графика", color=config['ui']['text_color'])

    ax.grid(True, linestyle='--', alpha=0.6)
    canvas.draw()


def update_status_bar(label, last_update_time):
    """Обновляет текст в статус-баре."""
    time_str = last_update_time.strftime('%H:%M:%S')
    label.config(text=f"Последнее обновление: {time_str}")


# --- Пример запуска окна (для отладки) ---
if __name__ == '__main__':
    print("--- Тестирование модуля ui_manager.py ---")

    # Для теста нам нужен макет конфига
    mock_config = {
        'ui': {
            'background_color': '#f0f0f0', 'text_color': '#000000',
            'success_color': '#2a9d8f', 'anomaly_color': '#e76f51',
            'graph_line_color': '#0077b6', 'font_family': 'Calibri', 'font_size': 10
        }
    }

    root = create_main_window(mock_config)
    create_styles(mock_config)
    frames = create_frames(root, mock_config)
    widgets = create_widgets(frames, mock_config)

    print("Окно успешно создано. Для проверки оно будет запущено.")
    print("Вы можете увидеть макет приложения. Закройте окно для продолжения.")

    # Демонстрация обновления
    update_status_bar(widgets['status_label'], datetime.now())

    # Добавим тестовые данные в таблицы
    import pandas as pd

    test_data = pd.DataFrame([
        {'symbol': 'BTC/USDT', 'price': 65000.1234},
        {'symbol': 'ETH/USDT', 'price': 3500.5678}
    ])
    update_prices_table(widgets['prices_tree'], test_data, [], mock_config)

    test_anomaly = {
        'symbol': 'XRP/USDT', 'price': 1.5, 'lower_bound': 0.4, 'upper_bound': 0.6
    }
    update_anomaly_log(widgets['anomaly_tree'], test_anomaly)

    root.mainloop()
