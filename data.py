import json
import logging

logging.basicConfig(level=logging.INFO)

class Note:
    """
    Класс, представляющий заметку.

    Атрибуты:
    title (str): Заголовок заметки.
    content (str): Содержимое заметки.
    category (str): Категория заметки.
    """
    def __init__(self, title, content, category=None):
        self.title = title
        self.content = content
        self.category = category if category else "Uncategorized"

    def __repr__(self):
        return f"Note({self.title}, {len(self.content)} chars, {self.category})"

class NoteManager:
    """
    Класс для управления заметками.

    Атрибуты:
    notes (dict): Словарь с заметками, организованными по категориям.
    """
    def __init__(self):
        self.notes = {}

    def add_note(self, title, content, category=None):
        """
        Добавляет новую заметку.

        Аргументы:
        title (str): Заголовок заметки.
        content (str): Содержимое заметки.
        category (str, optional): Категория заметки. По умолчанию None.

        Возвращает:
        Note: Созданная заметка.
        """
        note = Note(title, content, category)
        if category not in self.notes:
            self.notes[category] = []
        self.notes[category].append(note)
        logging.info(f"Note added: {note}")
        return note

    def delete_note(self, category, index):
        """
        Удаляет заметку по индексу в указанной категории.

        Аргументы:
        category (str): Категория заметки.
        index (int): Индекс заметки для удаления.
        """
        if category in self.notes and 0 <= index < len(self.notes[category]):
            deleted_note = self.notes[category].pop(index)
            logging.info(f"Note deleted: {deleted_note}")

    def update_note(self, category, index, title, content):
        """
        Обновляет заметку по индексу в указанной категории.

        Аргументы:
        category (str): Категория заметки.
        index (int): Индекс заметки для обновления.
        title (str): Новый заголовок заметки.
        content (str): Новое содержимое заметки.
        """
        if category in self.notes and 0 <= index < len(self.notes[category]):
            note = self.notes[category][index]
            note.title = title
            note.content = content
            logging.info(f"Note updated: {note}")

    def get_notes(self, category):
        """
        Возвращает список заметок в указанной категории.

        Аргументы:
        category (str): Категория заметок.

        Возвращает:
        list: Список заметок в категории.
        """
        return self.notes.get(category, [])

    def get_note_content(self, category, index):
        """
        Возвращает содержимое заметки по индексу в указанной категории.

        Аргументы:
        category (str): Категория заметки.
        index (int): Индекс заметки.

        Возвращает:
        str: Содержимое заметки.
        """
        if category in self.notes and 0 <= index < len(self.notes[category]):
            return self.notes[category][index].content
        return ""

    def save_to_file(self, filename):
        """
        Сохраняет заметки в файл.

        Аргументы:
        filename (str): Имя файла для сохранения.
        """
        with open(filename, 'w') as file:
            json.dump({category: [note.__dict__ for note in notes] for category, notes in self.notes.items()}, file)
            logging.info(f"Notes saved to {filename}")

    def load_from_file(self, filename):
        """
        Загружает заметки из файла.

        Аргументы:
        filename (str): Имя файла для загрузки.
        """
        try:
            with open(filename, 'r') as file:
                notes_data = json.load(file)
                if isinstance(notes_data, list):  # Старый формат, просто список заметок
                    self.notes = {}
                    for note in notes_data:
                        category = note.get("category", "Uncategorized")
                        if category not in self.notes:
                            self.notes[category] = []
                        self.notes[category].append(Note(
                            title=note["title"],
                            content=note["content"],
                            category=category
                        ))
                else:  # Новый формат, организованный по категориям
                    self.notes = {category: [Note(**note) for note in notes] for category, notes in notes_data.items()}
                logging.info(f"Notes loaded from {filename}")
        except FileNotFoundError:
            logging.info(f"File {filename} not found. Starting with an empty note list.")

    def __repr__(self):
        return f"NoteManager({len(self.notes)} categories, {sum(len(notes) for notes in self.notes.values())} notes)"
