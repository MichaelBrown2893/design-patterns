import os

import pytest

from single_responsibility import Journal, PersistenceManager


# region fixtures
@pytest.fixture
def journal():
    j = Journal()
    return j


@pytest.fixture
def entry():
    entry = "Hello"
    return entry


# endregion


# region Journal tests
def test_journal_add_entry_adds_entry(journal, entry):
    assert not journal.entries
    journal.add_entry(text=entry)
    assert entry in journal.entries


def test_journal_remove_entry_removes_entry(journal, entry):
    journal.add_entry(text=entry)
    assert entry in journal.entries
    journal.remove_entry(entry_num=0)
    assert not journal.entries


# endregion

# region PersistenceManager tests
def test_save_to_file_writes_to_file(journal, entry):
    journal.add_entry(text=entry)
    filepath = f"{os.getcwd()}/test_file.txt"
    PersistenceManager.save_to_file(journal=journal, path=filepath)
    with open(filepath, "r", encoding="UTF-8") as file:
        assert file.read() == f'1: {entry}'
    os.remove(filepath)

# endregion
