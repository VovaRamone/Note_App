import pytest
from data import NoteManager

def test_add_note():
    manager = NoteManager()
    note = manager.add_note("Test Note", "This is a test note.", "Test Category")
    assert note.title == "Test Note"
    assert note.content == "This is a test note."
    assert note.category == "Test Category"
    assert len(manager.get_notes("Test Category")) == 1

def test_delete_note():
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    manager.delete_note("Test Category", 0)
    assert len(manager.get_notes("Test Category")) == 0

def test_update_note():
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    manager.update_note("Test Category", 0, "Updated Note", "This is an updated note.")
    note = manager.get_notes("Test Category")[0]
    assert note.title == "Updated Note"
    assert note.content == "This is an updated note."

def test_get_note_content():
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    content = manager.get_note_content("Test Category", 0)
    assert content == "This is a test note."

def test_export_import_notes(tmpdir):
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    filename = tmpdir.join("notes.json")
    manager.save_to_file(filename)
    assert filename.check()

    new_manager = NoteManager()
    new_manager.load_from_file(filename)
    assert len(new_manager.get_notes("Test Category")) == 1
    assert new_manager.get_notes("Test Category")[0].title == "Test Note"

def test_edit_note_title():
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    manager.update_note("Test Category", 0, "Edited Note", "This is a test note.")
    note = manager.get_notes("Test Category")[0]
    assert note.title == "Edited Note"

def test_edit_note_category():
    manager = NoteManager()
    manager.add_note("Test Note", "This is a test note.", "Test Category")
    manager.update_note("Test Category", 0, "Test Note", "This is a test note.")
    note = manager.get_notes("Test Category")[0]
    assert note.category == "Test Category"
    manager.add_note("Another Note", "This is another note.", "Another Category")
    note_to_edit = manager.get_notes("Test Category")[0]
    note_to_edit.category = "Another Category"
    assert note_to_edit.category == "Another Category"

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
