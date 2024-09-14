import datetime
import tkinter as tk
import customtkinter
from tkinter import filedialog, simpledialog
import sys
import os
from music_player import play_mp3, stop_music  # Импортируем функции play_mp3 и stop_music

# Текущая приписка
current_label_index = 0
labels = ["Вопрос", "Ответ"]

# Начальный размер шрифта
font_size = 14

# Добавим переменную для текущего языка
current_language_index = 0
languages = ["ru", "en", "fr"]  # Добавьте другие языки по мере необходимости

# Словарь для хранения переводов
translations = {
    "ru": {
        "open_file": "Открыть файл",
        "save_file": "Сохранить Файл",
        "font_size": "Размер Шрифта",
        "change_language": "Сменить Язык",
        "entry_placeholder": "Ввведи в меня немного текста, дорогой!",
        "labels": ["Вопрос", "Ответ"]
    },
    "en": {
        "open_file": "Open File",
        "save_file": "Save File",
        "font_size": "Font Size",
        "change_language": "Change Language",
        "entry_placeholder": "Enter some text, please!",
        "labels": ["Question", "Answer"]
    },
    "fr": {
        "open_file": "Ouvrir le fichier",
        "save_file": "Enregistrer le fichier",
        "font_size": "Taille de la police",
        "change_language": "Changer de langue >RU",
        "entry_placeholder": "Entrez un peu de texte, s'il vous plaît!",
        "labels": ["Question", "Réponse"]
    }
}

def change_language():
    global current_language_index
    current_language_index = (current_language_index + 1) % len(languages)
    current_language = languages[current_language_index]

    # Обновить текст кнопок и меток
    open_button.configure(text=translations[current_language]["open_file"])
    save_button.configure(text=translations[current_language]["save_file"])
    change_font_button.configure(text=translations[current_language]["font_size"])
    change_language_button.configure(text=translations[current_language]["change_language"])
    label.configure(text=translations[current_language]["labels"][current_label_index])
    entry.configure(placeholder_text=translations[current_language]["entry_placeholder"])

def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def save_text(event=None):
    global current_label_index
    # Проверка, открыт ли файл
    if not file_path:
        show_warning("Ты файл то для начала открой!")
        return

    # Получить ввод пользователя
    user_input = entry.get()

    # Получить текущую дату и время
    now = datetime.datetime.now()

    # Форматировать дату и время
    formatted_now = now.strftime("[%H:%M:%S]")

    # Записать дату, время, приписку и ввод пользователя в файл
    with open(file_path, 'a') as f:
        f.write(f"{formatted_now} - {labels[current_label_index]} - {user_input}\n")

    # Очистить поле ввода
    entry.delete(0, tk.END)

    # Обновить текстовое поле содержимым файла
    update_text_box()

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt")
    if file_path:
        update_text_box()

def save_file():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        update_text_box()

def update_text_box():
    # Clear the text box
    text_box.delete(1.0, tk.END)

    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            parts = line.split(' - ', 2)
            if len(parts) == 3:
                timestamp, label, text = parts
                label = label.strip()
                text_box.insert(tk.END, f"{timestamp} - ", "timestamp")
                text_box.insert(tk.END, f"{label} - ", "question" if label == "Вопрос" else "answer")
                text_box.insert(tk.END, f"{text}\n", "question" if label == "Вопрос" else "answer")
            else:
                text_box.insert(tk.END, line + "\n\n")

    # Scroll to the end of the text
    text_box.see(tk.END)

def change_label(event):
    global current_label_index
    if event.keysym == 'Up':
        current_label_index = (current_label_index - 1) % len(labels)
    elif event.keysym == 'Down':
        current_label_index = (current_label_index + 1) % len(labels)

    current_label = labels[current_label_index]
    label_color = "#dc6250" if current_label == "Вопрос" else "#2152a5"

    # Update the label text and color
    label.configure(text=current_label, text_color=label_color)
    # Update the color of the corresponding text in the textbox
    text_box.tag_configure("question", foreground="#dc6250")
    text_box.tag_configure("answer", foreground="#2152a5")

def select_all(event=None):
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    return "break"

def show_warning(message):
    warning_window = customtkinter.CTkToplevel(root)
    warning_window.title("Предупреждение!")

    # Установить размер окна
    warning_window.geometry("800x600")

    # Разместить окно по центру экрана
    warning_window.update_idletasks()
    width = warning_window.winfo_width()
    height = warning_window.winfo_height()
    x = (warning_window.winfo_screenwidth() // 2) - (width // 2)
    y = (warning_window.winfo_screenheight() // 2) - (height // 2)

    # Сделать окно поверх всех окон
    warning_window.attributes("-topmost", True)

    warning_label = customtkinter.CTkLabel(master=warning_window, text=message)
    warning_label.pack(pady=20, padx=20)
    ok_button = customtkinter.CTkButton(master=warning_window, text="OK", command=warning_window.destroy)
    ok_button.pack(pady=10, padx=10)

def change_font_size():
    global font_size
    new_size = simpledialog.askinteger("Размер Шрифта", "Размер Шрифта:", initialvalue=font_size)
    if new_size:
        font_size = new_size
        update_font_size()

def update_font_size():
    global font_size
    arial_font = ("Arial", font_size)

    # Обновить шрифт для всех виджетов
    open_button.configure(font=arial_font)
    save_button.configure(font=arial_font)
    change_font_button.configure(font=arial_font)
    text_box.configure(font=arial_font)
    text_box.tag_configure("question", foreground="#dc6250", font=arial_font)
    text_box.tag_configure("answer", foreground="#2152a5", font=arial_font)
    text_box.tag_configure("timestamp", foreground="#eeb24a", font=arial_font)
    if labels[current_label_index] == "Вопрос":
        text_box.tag_configure("label", foreground="#dc6250", font=(arial_font[0], arial_font[1]))
    elif labels[current_label_index] == "Ответ":
        text_box.tag_configure("label", foreground="#2152a5", font=(arial_font[0], arial_font[1]))
    label.configure(font=arial_font)
    entry.configure(font=arial_font)

def on_closing():
    stop_music()
    root.destroy()

# Установить режим внешнего вида и цветовую тему
customtkinter.set_appearance_mode("dark")  # Режимы: system (по умолчанию), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Тема: blue (по умолчанию), dark-blue, green

# Создать главное окно
root = customtkinter.CTk()
root.title("Стенограф")

# Установить шрифт Arial для всех виджетов
arial_font = ("Arial", font_size)

# Создать контейнер для кнопок
nav_frame = customtkinter.CTkFrame(master=root)
nav_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

# Создать кнопку для открытия файла
open_button = customtkinter.CTkButton(master=nav_frame, text="Открыть файл", command=open_file, font=arial_font, fg_color="#55927f", text_color="black")
open_button.pack(side=tk.LEFT, padx=5)

# Создать кнопку для сохранения файла
save_button = customtkinter.CTkButton(master=nav_frame, text="Сохранить Файл", command=save_file, font=arial_font, fg_color="#55927f", text_color="black")
save_button.pack(side=tk.LEFT, padx=5)

# Создать кнопку для изменения размера шрифта
change_font_button = customtkinter.CTkButton(master=nav_frame, text="Размер Шрифта", command=change_font_size, font=arial_font, fg_color="#55927f", text_color="black")
change_font_button.pack(side=tk.LEFT, padx=5)

change_language_button = customtkinter.CTkButton(master=nav_frame, text=translations[languages[current_language_index]]["change_language"], command=change_language, font=arial_font, fg_color="#55927f", text_color="black")
change_language_button.pack(side=tk.LEFT, padx=5)

# Создать текстовое поле для отображения содержимого файла
text_box = tk.Text(root, state=tk.NORMAL, bg="#272a32", fg="#abb2bf", font=arial_font)
text_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Настройка тегов для разных цветов текста
text_box.tag_configure("question", foreground="#dc6250", font=arial_font)
text_box.tag_configure("answer", foreground="#2152a5", font=arial_font)
text_box.tag_configure("timestamp", foreground="#eeb24a", font=arial_font)

# Создать контейнер для метки и поля ввода
input_frame = customtkinter.CTkFrame(master=root)
input_frame.pack(pady=10, padx=10, fill=tk.X)

# Создать метку для отображения текущей приписки
label = customtkinter.CTkLabel(master=input_frame, text=labels[current_label_index], width=10, font=arial_font)
label.pack(side=tk.LEFT, padx=5)

# Создать поле ввода для пользователя
entry = customtkinter.CTkEntry(master=input_frame, placeholder_text="Ввведи в меня немного текста, дорогой!", font=arial_font)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
entry.bind("<Return>", save_text)
entry.bind("<Up>", change_label)
entry.bind("<Down>", change_label)
entry.bind("<Control-a>", select_all)
entry.bind("<Control-A>", select_all)

# Установить начальный путь к файлу
file_path = ""

# Запустить воспроизведение музыки
play_mp3(get_path("music.mp3"))  # Используем функцию get_path для получения правильного пути

# Установить иконку приложения
root.iconbitmap(get_path('icon.ico'))

# Добавить обработчик события закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)

# Запустить основной цикл
root.mainloop()
