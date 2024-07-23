import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, ttk, font
import logging
from data import NoteManager
from utils import search_notes

logging.basicConfig(level=logging.INFO)

class NoteApp:
    """
    Класс для создания и управления графическим интерфейсом приложения заметок.

    Атрибуты:
    root (tk.Tk): Корневой виджет Tkinter.
    manager (NoteManager): Экземпляр класса NoteManager для управления заметками.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Note Application")
        self.root.geometry("1920x1080")
        self.manager = NoteManager()
        self.categories = []
        self.selected_category = None
        self.selected_note_index = None
        self.autosave_enabled = tk.BooleanVar(value=False)

        self.setup_ui()
        self.load_notes()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_ui(self):
        """
        Настройка пользовательского интерфейса.
        """
        # Настройка шрифта и цветов
        custom_font = font.Font(family="Helvetica", size=12)
        bg_color = "#f0f0f0"
        btn_color = "#4CAF50"
        btn_font_color = "#ffffff"

        self.root.configure(bg=bg_color)

        self.text_area = tk.Text(self.root, font=custom_font, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both', padx=10, pady=10)
        self.text_area.bind("<KeyRelease>", lambda event: self.autosave())

        self.button_frame = tk.Frame(self.root, bg=bg_color)
        self.button_frame.pack(fill='x')

        button_config = {
            "bg": btn_color,
            "fg": btn_font_color,
            "font": custom_font,
            "activebackground": "#45a049",
            "activeforeground": "#ffffff",
            "relief": tk.FLAT
        }

        self.add_button = tk.Button(self.button_frame, text="Add Note", command=self.add_note_dialog, **button_config)
        self.add_button.pack(side='left', padx=5, pady=5)

        self.save_button = tk.Button(self.button_frame, text="Save Note", command=self.save_note, **button_config)
        self.save_button.pack(side='left', padx=5, pady=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete Note", command=self.delete_note, **button_config)
        self.delete_button.pack(side='left', padx=5, pady=5)

        self.export_button = tk.Button(self.button_frame, text="Export Notes", command=self.export_notes, **button_config)
        self.export_button.pack(side='left', padx=5, pady=5)

        self.import_button = tk.Button(self.button_frame, text="Import Notes", command=self.import_notes, **button_config)
        self.import_button.pack(side='left', padx=5, pady=5)

        self.edit_title_button = tk.Button(self.button_frame, text="Edit Title", command=self.edit_title, **button_config)
        self.edit_title_button.pack(side='left', padx=5, pady=5)

        self.edit_category_button = tk.Button(self.button_frame, text="Edit Category", command=self.edit_category, **button_config)
        self.edit_category_button.pack(side='left', padx=5, pady=5)

        self.category_button = tk.Button(self.button_frame, text="Add Category", command=self.add_category_dialog, **button_config)
        self.category_button.pack(side='left', padx=5, pady=5)

        self.edit_category_name_button = tk.Button(self.button_frame, text="Edit Category Name", command=self.edit_category_name, **button_config)
        self.edit_category_name_button.pack(side='left', padx=5, pady=5)

        self.delete_category_button = tk.Button(self.button_frame, text="Delete Category", command=self.delete_category, **button_config)
        self.delete_category_button.pack(side='left', padx=5, pady=5)

        self.search_label = tk.Label(self.button_frame, text="Search:", font=custom_font, bg=bg_color)
        self.search_label.pack(side='left', padx=5, pady=5)

        self.search_entry = tk.Entry(self.button_frame, font=custom_font)
        self.search_entry.pack(side='left', padx=5, pady=5)

        self.search_button = tk.Button(self.button_frame, text="Search", command=self.search_notes, **button_config)
        self.search_button.pack(side='left', padx=5, pady=5)

        self.autosave_checkbutton = tk.Checkbutton(self.button_frame, text="Autosave", variable=self.autosave_enabled, bg=bg_color, font=custom_font)
        self.autosave_checkbutton.pack(side='left', padx=5, pady=5)

        self.category_frame = tk.Frame(self.root, bg=bg_color)
        self.category_frame.pack(side='left', fill='y', padx=10, pady=10)

        self.category_listbox = tk.Listbox(self.category_frame, font=custom_font)
        self.category_listbox.pack(fill='y', expand=True)
        self.category_listbox.bind("<<ListboxSelect>>", self.display_category_notes)

        self.note_frame = tk.Frame(self.root, bg=bg_color)
        self.note_frame.pack(side='right', fill='y', padx=10, pady=10)

        self.note_listbox = tk.Listbox(self.note_frame, font=custom_font)
        self.note_listbox.pack(fill='y', expand=True)
        self.note_listbox.bind("<<ListboxSelect>>", self.display_note)

    def add_note_dialog(self):
        """
        Открывает диалог для добавления новой заметки.
        """
        if not self.categories:
            self.add_category_dialog()

        dialog = tk.Toplevel(self.root)
        dialog.title("Add Note")
        dialog.configure(bg="#ffffff")

        tk.Label(dialog, text="Title:", bg="#ffffff").pack(pady=5)
        title_entry = tk.Entry(dialog, font=("Helvetica", 10))
        title_entry.pack(pady=5)

        tk.Label(dialog, text="Category:", bg="#ffffff").pack(pady=5)
        category_combo = ttk.Combobox(dialog, values=self.categories)
        category_combo.pack(pady=5)

        tk.Button(dialog, text="Add Category", command=lambda: self.add_category_dialog(category_combo)).pack(pady=5)

        def on_ok():
            title = title_entry.get()
            category = category_combo.get()
            if not title or not category:
                messagebox.showerror("Error", "Title and category are required")
                return
            self.manager.add_note(title, "", category)
            self.note_listbox.insert(tk.END, title)
            dialog.destroy()
            self.autosave()

        def on_cancel():
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok).pack(side='left', padx=5, pady=5)
        tk.Button(dialog, text="Cancel", command=on_cancel).pack(side='right', padx=5, pady=5)

    def add_category_dialog(self, combo=None):
        """
        Открывает диалог для добавления новой категории.
        """
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Category")
        dialog.configure(bg="#ffffff")

        tk.Label(dialog, text="Category Name:", bg="#ffffff").pack(pady=5)
        category_entry = tk.Entry(dialog, font=("Helvetica", 10))
        category_entry.pack(pady=5)

        def on_ok():
            category = category_entry.get()
            if not category:
                messagebox.showerror("Error", "Category name is required")
                return
            if category not in self.categories:
                self.categories.append(category)
                self.category_listbox.insert(tk.END, category)
                if combo:
                    combo['values'] = self.categories
            dialog.destroy()
            self.autosave()

        def on_cancel():
            dialog.destroy()

        tk.Button(dialog, text="OK", command=on_ok).pack(side='left', padx=5, pady=5)
        tk.Button(dialog, text="Cancel", command=on_cancel).pack(side='right', padx=5, pady=5)

    def save_note(self):
        """
        Сохраняет текущую заметку.
        """
        if self.selected_category and self.selected_note_index is not None:
            content = self.text_area.get("1.0", tk.END).strip()
            self.manager.update_note(self.selected_category, self.selected_note_index, self.manager.notes[self.selected_category][self.selected_note_index].title, content)
            messagebox.showinfo("Info", "Note saved successfully!")
            logging.info(f"Note saved: {self.manager.notes[self.selected_category][self.selected_note_index]}")
            self.autosave()

    def delete_note(self):
        """
        Удаляет выбранную заметку.
        """
        if self.selected_category and self.selected_note_index is not None:
            self.manager.delete_note(self.selected_category, self.selected_note_index)
            self.note_listbox.delete(self.selected_note_index)
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Info", "Note deleted successfully!")
            logging.info(f"Note deleted at index: {self.selected_note_index}")
            self.autosave()

    def display_note(self, event):
        """
        Отображает содержимое выбранной заметки.
        """
        selected_note_index = self.note_listbox.curselection()
        if selected_note_index:
            self.selected_note_index = selected_note_index[0]
            note_content = self.manager.get_note_content(self.selected_category, self.selected_note_index)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, note_content)
            logging.info(f"Displaying note at index: {self.selected_note_index}")

    def display_category_notes(self, event):
        """
        Отображает заметки выбранной категории.
        """
        selected_category_index = self.category_listbox.curselection()
        if selected_category_index:
            self.selected_category = self.categories[selected_category_index[0]]
            self.note_listbox.delete(0, tk.END)
            notes = self.manager.get_notes(self.selected_category)
            for note in notes:
                self.note_listbox.insert(tk.END, note.title)

    def export_notes(self):
        """
        Экспортирует заметки в файл JSON.
        """
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            self.manager.save_to_file(filename)
            messagebox.showinfo("Info", "Notes exported successfully!")
            logging.info(f"Notes exported to {filename}")

    def import_notes(self):
        """
        Импортирует заметки из файла JSON.
        """
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            self.manager.load_from_file(filename)
            self.category_listbox.delete(0, tk.END)
            self.note_listbox.delete(0, tk.END)
            self.categories = list(self.manager.notes.keys())
            for category in self.categories:
                self.category_listbox.insert(tk.END, category)
            messagebox.showinfo("Info", "Notes imported successfully!")
            logging.info(f"Notes imported from {filename}")
            self.autosave()

    def search_notes(self):
        """
        Выполняет поиск по заметкам.
        """
        query = self.search_entry.get().strip()
        if query:
            results = search_notes([note for notes in self.manager.notes.values() for note in notes], query)
            self.note_listbox.delete(0, tk.END)
            for note in results:
                self.note_listbox.insert(tk.END, note.title)
            logging.info(f"Search performed with query: {query}")

    def edit_title(self):
        """
        Редактирует заголовок выбранной заметки.
        """
        if self.selected_category and self.selected_note_index is not None:
            new_title = simpledialog.askstring("Input", "Enter new title:", parent=self.root)
            if new_title:
                self.manager.notes[self.selected_category][self.selected_note_index].title = new_title
                self.note_listbox.delete(self.selected_note_index)
                self.note_listbox.insert(self.selected_note_index, new_title)
                logging.info(f"Note title updated to: {new_title}")
                self.autosave()

    def edit_category(self):
        """
        Редактирует категорию выбранной заметки.
        """
        if self.selected_category and self.selected_note_index is not None:
            new_category = simpledialog.askstring("Input", "Enter new category:", parent=self.root)
            if new_category:
                note = self.manager.notes[self.selected_category].pop(self.selected_note_index)
                note.category = new_category
                if new_category not in self.manager.notes:
                    self.manager.notes[new_category] = []
                self.manager.notes[new_category].append(note)
                self.note_listbox.delete(self.selected_note_index)
                if not self.manager.notes[self.selected_category]:
                    self.categories.remove(self.selected_category)
                    self.category_listbox.delete(self.selected_category)
                self.selected_category = new_category
                self.display_category_notes(None)
                logging.info(f"Note category updated to: {new_category}")
                self.autosave()

    def edit_category_name(self):
        """
        Редактирует название выбранной категории.
        """
        selected_category_index = self.category_listbox.curselection()
        if selected_category_index:
            old_category = self.categories[selected_category_index[0]]
            new_category = simpledialog.askstring("Input", "Enter new category name:", parent=self.root)
            if new_category and new_category not in self.categories:
                notes = self.manager.notes.pop(old_category)
                for note in notes:
                    note.category = new_category
                self.manager.notes[new_category] = notes
                self.categories[selected_category_index[0]] = new_category
                self.category_listbox.delete(selected_category_index[0])
                self.category_listbox.insert(selected_category_index[0], new_category)
                if self.selected_category == old_category:
                    self.selected_category = new_category
                messagebox.showinfo("Info", f"Category '{old_category}' renamed to '{new_category}' successfully!")
                logging.info(f"Category '{old_category}' renamed to '{new_category}'")
                self.autosave()

    def delete_category(self):
        """
        Удаляет выбранную категорию.
        """
        selected_category_index = self.category_listbox.curselection()
        if selected_category_index:
            category_to_delete = self.categories[selected_category_index[0]]
            self.categories.pop(selected_category_index[0])
            self.category_listbox.delete(selected_category_index[0])
            del self.manager.notes[category_to_delete]
            self.note_listbox.delete(0, tk.END)
            self.text_area.delete("1.0", tk.END)
            messagebox.showinfo("Info", f"Category '{category_to_delete}' deleted successfully!")
            logging.info(f"Category '{category_to_delete}' deleted")
            self.autosave()

    def load_notes(self):
        """
        Загружает заметки из файла при запуске приложения.
        """
        self.manager.load_from_file("notes.json")
        for category in self.manager.notes.keys():
            self.category_listbox.insert(tk.END, category)
        self.categories = list(self.manager.notes.keys())
        logging.info("Notes loaded at startup.")

    def save_notes(self):
        """
        Сохраняет заметки в файл при закрытии приложения.
        """
        self.manager.save_to_file("notes.json")
        logging.info("Notes saved at shutdown.")

    def autosave(self):
        """
        Автосохранение заметок.
        """
        if self.autosave_enabled.get():
            self.save_notes()

    def on_closing(self):
        """
        Событие закрытия приложения, сохраняет заметки.
        """
        self.save_notes()
        self.root.destroy()
