from ttm_scripts import get_script_for_step
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import json
import os
import keyboard
import threading

class TTMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TTM Automation Pro")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Переменные для хранения настроек
        self.settings = {
            "hotkey": "ctrl+shift+1",
            "day": "Sat",
            "zone": "Stand A",
            "ticket_count": "6",
            "names": ["Chiraphat chaikhuntod", "Ya Eby Tvoyu Mat", "32131 3231", "", "", ""]
        }
        
        # Загрузка сохраненных настроек
        self.load_settings()
        
        # Текущий шаг
        self.current_step = 0
        
        # Создание интерфейса
        self.create_gui()
        
        # Создание последовательности скриптов
        self.update_sequence()
        
        # Запуск обработки горячих клавиш в отдельном потоке
        self.hotkey_thread = threading.Thread(target=self.setup_hotkeys, daemon=True)
        self.hotkey_thread.start()
        
    def create_gui(self):
        # Создание вкладок
        tab_control = ttk.Notebook(self.root)
        
        tab_settings = ttk.Frame(tab_control)
        tab_sequence = ttk.Frame(tab_control)
        tab_control.add(tab_settings, text='Настройки')
        tab_control.add(tab_sequence, text='Последовательность')
        tab_control.pack(expand=1, fill='both')
        
        # Настройки
        self.create_settings_tab(tab_settings)
        
        # Последовательность
        self.create_sequence_tab(tab_sequence)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("Готов к работе")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_settings_tab(self, parent):
        # Горячая клавиша
        tk.Label(parent, text="Горячая клавиша:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.hotkey_var = tk.StringVar(value=self.settings["hotkey"])
        hotkey_combo = ttk.Combobox(parent, textvariable=self.hotkey_var, 
                                   values=["ctrl+shift+1", "ctrl+shift+2", "ctrl+shift+3", 
                                           "ctrl+shift+4", "ctrl+shift+5", "ctrl+shift+6",
                                           "alt+shift+1", "alt+shift+2", "alt+shift+3"])
        hotkey_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # День недели
        tk.Label(parent, text="День недели:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.day_var = tk.StringVar(value=self.settings["day"])
        day_combo = ttk.Combobox(parent, textvariable=self.day_var, 
                                values=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
        day_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Зона
        tk.Label(parent, text="Зона:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.zone_var = tk.StringVar(value=self.settings["zone"])
        zone_combo = ttk.Combobox(parent, textvariable=self.zone_var, 
                                 values=["Stand A", "Stand B", "SC", "SD", "SM", "SL"])
        zone_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        zone_combo.bind("<<ComboboxSelected>>", self.on_zone_change)
        
        # Количество билетов
        tk.Label(parent, text="Количество билетов:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.ticket_count_var = tk.StringVar(value=self.settings["ticket_count"])
        ticket_combo = ttk.Combobox(parent, textvariable=self.ticket_count_var, 
                                   values=["1", "2", "3", "4", "5", "6"])
        ticket_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Имена
        tk.Label(parent, text="Имена для заполнения:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_vars = []
        name_frame = tk.Frame(parent)
        name_frame.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        
        for i in range(6):
            tk.Label(name_frame, text=f"Имя {i+1}:").grid(row=i, column=0, sticky=tk.W, padx=2, pady=2)
            name_var = tk.StringVar(value=self.settings["names"][i] if i < len(self.settings["names"]) else "")
            entry = tk.Entry(name_frame, textvariable=name_var, width=20)
            entry.grid(row=i, column=1, sticky=tk.W, padx=2, pady=2)
            self.name_vars.append(name_var)
        
        # Кнопки
        button_frame = tk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="Сохранить настройки", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Обновить последовательность", command=self.update_sequence).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Сбросить шаги", command=self.reset_steps).pack(side=tk.LEFT, padx=5)
        
    def create_sequence_tab(self, parent):
        # Поле для отображения последовательности
        self.sequence_text = tk.Text(parent, wrap=tk.WORD, height=20)
        scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.sequence_text.yview)
        self.sequence_text.configure(yscrollcommand=scrollbar.set)
        
        self.sequence_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Кнопка для копирования текущего шага
        tk.Button(parent, text="Копировать текущий шаг", command=self.copy_current_step).pack(pady=5)
        
    def on_zone_change(self, event):
        # Показываем/скрываем поля имен в зависимости от выбранной зоны
        zone = self.zone_var.get()
        if zone in ["Stand A", "Stand B"]:
            for i, var in enumerate(self.name_vars):
                if i >= 4:  # Скрываем поля 5 и 6
                    var.set("")
        self.update_sequence()
        
    def update_sequence(self):
        # Обновляем последовательность на основе текущих настроек
        zone = self.zone_var.get()
        ticket_count = self.ticket_count_var.get()
        
        sequence = []
        sequence.append("1. Подтверждение условий (1.confirm-terms.js)")
        sequence.append(f"2. Выбор даты: {self.day_var.get()} (2.select-show-date.js)")
        
        if zone == "Stand A":
            sequence.append("3. Выбор зоны Stand A (3.Alter-select-zone-A.js)")
        elif zone == "Stand B":
            sequence.append("3. Выбор зоны Stand B (3.Alter-select-zone-B.js)")
        else:
            sequence.append(f"3. Выбор зоны {zone} (3.select-zone-copy.js)")
        
        if zone in ["Stand A", "Stand B"]:
            sequence.append(f"4. Выбор {ticket_count} билетов (4.AlterSeatsCount.js)")
            sequence.append("5. Подтверждение оплаты (6.AlterPred3DS.js)")
        else:
            sequence.append(f"4. Выбор {ticket_count} мест (4.select-seats.js)")
            sequence.append("5. Заполнение данных имен (5.fill-details.js)")
            sequence.append("6. Подтверждение оплаты (6.AlterPred3DS.js)")
        
        # Обновляем текстовое поле
        self.sequence_text.delete(1.0, tk.END)
        for i, step in enumerate(sequence):
            status = "✓ " if i < self.current_step else "○ "
            self.sequence_text.insert(tk.END, f"{status}{step}\n")
        
        self.sequence_steps = sequence
        self.total_steps = len(sequence)
        
    def save_settings(self):
        # Сохраняем настройки
        self.settings = {
            "hotkey": self.hotkey_var.get(),
            "day": self.day_var.get(),
            "zone": self.zone_var.get(),
            "ticket_count": self.ticket_count_var.get(),
            "names": [var.get() for var in self.name_vars]
        }
        
        # Сохраняем в файл
        with open("ttm_settings.json", "w") as f:
            json.dump(self.settings, f)
        
        # Перезапускаем обработку горячих клавиш
        self.setup_hotkeys()
        
        self.status_var.set("Настройки сохранены и применены")
        
    def load_settings(self):
        # Загружаем настройки из файла
        try:
            with open("ttm_settings.json", "r") as f:
                self.settings = json.load(f)
        except FileNotFoundError:
            pass  # Используем настройки по умолчанию
            
    def setup_hotkeys(self):
        # Настраиваем горячие клавиши
        try:
            keyboard.unhook_all()  # Удаляем все предыдущие привязки
            
            # Добавляем новую привязку
            keyboard.add_hotkey(self.settings["hotkey"], self.next_step)
            
            self.status_var.set(f"Горячая клавиша: {self.settings['hotkey']}")
        except Exception as e:
            self.status_var.set(f"Ошибка настройки горячей клавиши: {str(e)}")
            
    def next_step(self):
        # Переходим к следующему шагу
        if self.current_step < self.total_steps:
            self.current_step += 1
            self.update_sequence()
            self.copy_current_step()
            
    def copy_current_step(self):
        # Копируем скрипт текущего шага в буфер обмена
        if self.current_step <= self.total_steps:
            script = self.get_script_for_step(self.current_step)
            pyperclip.copy(script)
            self.status_var.set(f"Скрипт шага {self.current_step} скопирован в буфер обмена")
        else:
            self.status_var.set("Все шаги выполнены")
            
    def get_script_for_step(self, step):
        """Возвращаем скрипт для указанного шага"""
        zone = self.zone_var.get()
        
        # Определяем реальный номер шага для библиотеки скриптов
        if zone in ["Stand A", "Stand B"]:
            # Для Stand A/B пропускаем шаг 5 (заполнение имен)
            if step == 5:  # Это 5-й шаг в интерфейсе
                real_step = 6  # Но в библиотеке это 6-й шаг
            else:
                real_step = step
        else:
            # Для других зон все шаги соответствуют
            real_step = step
        
        settings = {
            "zone": zone,
            "day": self.day_var.get(),
            "ticket_count": self.ticket_count_var.get(),
            "names": [var.get() for var in self.name_vars]
        }
        
        # ВЫЗОВ ФУНКЦИИ ИЗ БИБЛИОТЕКИ
        return get_script_for_step(real_step, settings)
        
    def reset_steps(self):
        # Сбрасываем шаги
        self.current_step = 0
        self.update_sequence()
        self.status_var.set("Шаги сброшены")
        
    def run(self):
        # Запускаем главный цикл
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TTMApp(root)
    app.run()