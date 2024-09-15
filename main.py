import datetime
import tkinter as tk
import customtkinter
from tkinter import filedialog, simpledialog
import sys
import os
from music_player import play_mp3, stop_music  # Импортируем функции play_mp3 и stop_music

# Константы
FONT_SIZE = 14
LANGUAGES = ["ru", "en", "fr"]
TRANSLATIONS = {
    "ru": {
        "open_file": "Открыть файл",
        "save_file": "Сохранить Файл",
        "font_size": "Размер Шрифта",
        "change_language": "Сменить Язык",
        "entry_placeholder": "Введи в меня немного текста, дорогой!",
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
        "change_language": "Changer de langue",
        "entry_placeholder": "Entrez un peu de texte, s'il vous plaît!",
        "labels": ["Question", "Réponse"]
    }
}

class StenographerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Стенограф")
        self.current_label_index = 0
        self.current_language_index = 0
        self.font_size = FONT_SIZE
        self.file_path = ""

        self.setup_ui()
        self.update_translations()
        self.play_music()

    def setup_ui(self):
        self.arial_font = ("Arial", self.font_size)

        nav_frame = customtkinter.CTkFrame(master=self.root)
        nav_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=10)

        self.open_button = customtkinter.CTkButton(master=nav_frame, text="Открыть файл", command=self.open_file, font=self.arial_font, fg_color="#55927f", text_color="black")
        self.open_button.pack(side=tk.LEFT, padx=5)

        self.save_button = customtkinter.CTkButton(master=nav_frame, text="Сохранить Файл", command=self.save_file, font=self.arial_font, fg_color="#55927f", text_color="black")
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.change_font_button = customtkinter.CTkButton(master=nav_frame, text="Размер Шрифта", command=self.change_font_size, font=self.arial_font, fg_color="#55927f", text_color="black")
        self.change_font_button.pack(side=tk.LEFT, padx=5)

        self.change_language_button = customtkinter.CTkButton(master=nav_frame, text=TRANSLATIONS[LANGUAGES[self.current_language_index]]["change_language"], command=self.change_language, font=self.arial_font, fg_color="#55927f", text_color="black")
        self.change_language_button.pack(side=tk.LEFT, padx=5)

        self.text_box = tk.Text(self.root, state=tk.NORMAL, bg="#272a32", fg="#abb2bf", font=self.arial_font)
        self.text_box.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.text_box.tag_configure("question", foreground="#dc6250", font=self.arial_font)
        self.text_box.tag_configure("answer", foreground="#2152a5", font=self.arial_font)
        self.text_box.tag_configure("timestamp", foreground="#eeb24a", font=self.arial_font)

        input_frame = customtkinter.CTkFrame(master=self.root)
        input_frame.pack(pady=10, padx=10, fill=tk.X)

        self.label = customtkinter.CTkLabel(master=input_frame, text=TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"][self.current_label_index], width=10, font=self.arial_font)
        self.label.pack(side=tk.LEFT, padx=5)

        self.entry = customtkinter.CTkEntry(master=input_frame, placeholder_text=TRANSLATIONS[LANGUAGES[self.current_language_index]]["entry_placeholder"], font=self.arial_font)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", self.save_text)
        self.entry.bind("<Up>", self.change_label)
        self.entry.bind("<Down>", self.change_label)
        self.entry.bind("<Control-a>", self.select_all)
        self.entry.bind("<Control-A>", self.select_all)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_translations(self):
        current_language = LANGUAGES[self.current_language_index]
        self.open_button.configure(text=TRANSLATIONS[current_language]["open_file"])
        self.save_button.configure(text=TRANSLATIONS[current_language]["save_file"])
        self.change_font_button.configure(text=TRANSLATIONS[current_language]["font_size"])
        self.change_language_button.configure(text=TRANSLATIONS[current_language]["change_language"])
        self.label.configure(text=TRANSLATIONS[current_language]["labels"][self.current_label_index])
        self.entry.configure(placeholder_text=TRANSLATIONS[current_language]["entry_placeholder"])

    def change_language(self):
        self.current_language_index = (self.current_language_index + 1) % len(LANGUAGES)
        self.update_translations()
        self.show_warning("Пожалуйста, заново откройте файл.")

    def get_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def save_text(self, event=None):
        if not self.file_path:
            self.show_warning("Ты файл то для начала открой!")
            return

        user_input = self.entry.get()
        now = datetime.datetime.now()
        formatted_now = now.strftime("[%H:%M:%S]")

        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(f"{formatted_now} - {TRANSLATIONS[LANGUAGES[self.current_language_index]]['labels'][self.current_label_index]} - {user_input}\n")

        self.entry.delete(0, tk.END)
        self.update_text_box()

    def open_file(self):
        self.file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.file_path and not self.file_path.lower().endswith(".txt"):
            self.show_warning("Пожалуйста, выберите файл с расширением .txt")
            self.file_path = ""
        elif self.file_path:
            self.transcode_file_to_utf8()
            self.update_text_box()

    def save_file(self):
        self.file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.file_path and not self.file_path.lower().endswith(".txt"):
            self.show_warning("Пожалуйста, выберите файл с расширением .txt")
            self.file_path = ""
        elif self.file_path:
            self.update_text_box()

    def update_text_box(self):
        self.text_box.delete(1.0, tk.END)
        encodings = ['utf-8', 'cp1251', 'latin1']
        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                    for line in lines:
                        parts = line.split(' - ', 2)
                        if len(parts) == 3:
                            timestamp, label, text = parts
                            label = label.strip()
                            self.text_box.insert(tk.END, f"{timestamp} - ", "timestamp")
                            self.text_box.insert(tk.END, f"{label} - ", "question" if label == TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"][0] else "answer")
                            self.text_box.insert(tk.END, f"{text}\n", "question" if label == TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"][0] else "answer")
                        else:
                            self.text_box.insert(tk.END, line + "\n\n")
                self.text_box.see(tk.END)
                return
            except UnicodeDecodeError:
                continue
        self.show_warning("Не удалось открыть файл. Попробуйте другую кодировку.")

    def change_label(self, event):
        if event.keysym == 'Up':
            self.current_label_index = (self.current_label_index - 1) % len(TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"])
        elif event.keysym == 'Down':
            self.current_label_index = (self.current_label_index + 1) % len(TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"])

        current_label = TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"][self.current_label_index]
        label_color = "#dc6250" if current_label == TRANSLATIONS[LANGUAGES[self.current_language_index]]["labels"][0] else "#2152a5"
        self.label.configure(text=current_label, text_color=label_color)
        self.text_box.tag_configure("question", foreground="#dc6250")
        self.text_box.tag_configure("answer", foreground="#2152a5")

    def select_all(self, event=None):
        self.entry.select_range(0, tk.END)
        self.entry.icursor(tk.END)
        return "break"

    def show_warning(self, message):
        warning_window = customtkinter.CTkToplevel(self.root)
        warning_window.title("Предупреждение!")
        warning_window.geometry("800x600")
        warning_window.update_idletasks()
        width = warning_window.winfo_width()
        height = warning_window.winfo_height()
        x = (warning_window.winfo_screenwidth() // 2) - (width // 2)
        y = (warning_window.winfo_screenheight() // 2) - (height // 2)
        warning_window.attributes("-topmost", True)
        warning_label = customtkinter.CTkLabel(master=warning_window, text=message)
        warning_label.pack(pady=20, padx=20)
        ok_button = customtkinter.CTkButton(master=warning_window, text="OK", command=warning_window.destroy)
        ok_button.pack(pady=10, padx=10)

    def change_font_size(self):
        new_size = simpledialog.askinteger("Размер Шрифта", "Размер Шрифта:", initialvalue=self.font_size)
        if new_size:
            self.font_size = new_size
            self.update_font_size()

    def update_font_size(self):
        self.arial_font = ("Arial", self.font_size)
        self.open_button.configure(font=self.arial_font)
        self.save_button.configure(font=self.arial_font)
        self.change_font_button.configure(font=self.arial_font)
        self.text_box.configure(font=self.arial_font)
        self.text_box.tag_configure("question", foreground="#dc6250", font=self.arial_font)
        self.text_box.tag_configure("answer", foreground="#2152a5", font=self.arial_font)
        self.text_box.tag_configure("timestamp", foreground="#eeb24a", font=self.arial_font)
        self.label.configure(font=self.arial_font)
        self.entry.configure(font=self.arial_font)

    def on_closing(self):
        stop_music()
        self.root.destroy()

    def play_music(self):
        play_mp3(self.get_path("music.mp3"))

    def transcode_file_to_utf8(self):
        encodings = ['utf-8', 'cp1251', 'latin1']
        for encoding in encodings:
            try:
                with open(self.file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return
            except UnicodeDecodeError:
                continue
        self.show_warning("Не удалось открыть файл. Попробуйте другую кодировку.")

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    root = customtkinter.CTk()
    app = StenographerApp(root)
    root.iconbitmap(app.get_path('icon.ico'))
    root.mainloop()
