def search_notes(notes, query):
    """
    Ищет заметки по содержимому.

    Аргументы:
    notes (list): Список заметок.
    query (str): Строка поиска.

    Возвращает:
    list: Список заметок, содержащих строку поиска.
    """
    return [note for note in notes if query.lower() in note.content.lower()]
