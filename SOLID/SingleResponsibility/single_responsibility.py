""" single_responsibility.py

Single responsibility principle aka separation of concerns
File containing exercise from SRP udemy lecture

Creates a journal object
Adds entries to journal
Write journal to file
Read journal from file
"""
import os.path


class Journal:
    """Class responsible for storing journal entries"""

    entries: list[str]

    def __init__(self):
        """Constructor for Journal class"""
        self.entries = []

    def add_entry(self, text: str) -> None:
        """Records an entry in the journal

        :param text: Text for the journal entry
        """
        self.entries.append(f"{text}")

    def remove_entry(self, entry_num: int) -> None:
        """Removes an entry from the journal

        :param entry_num: Entry number of the entry to be removed (NOT INDEX)
        """
        del self.entries[entry_num - 1]

    def __str__(self) -> str:
        """Returns all entries from the journal listed with their index

        :return: Formatted entries from the journal as str
        """
        return "\n".join([f"{index + 1}: {entry}" for index, entry in enumerate(self.entries)])

    # Violates single responsibility principle should be handled separately
    # def save(self, path: str) -> None:
    #     """Writes the journal to a file
    #
    #     :param path: File to write the journal to
    #     """
    #     with open(path, 'w', encoding='UTF-8') as file:
    #         file.write(str(self))


class PersistenceManager:
    """Class responsible for managing persistence"""

    @staticmethod
    def save_to_file(journal: Journal, path: str) -> None:
        """Writes a journal to a file

        :param journal: The journal to be written to file
        :param path: The path of the file to write the journal to
        """
        with open(path, "w", encoding="UTF-8") as save_file:
            save_file.write(str(journal))


if __name__ == "__main__":
    j = Journal()
    j.add_entry("I cried today.")
    j.add_entry("I ate a bug.")
    print(f"Journal entries:\n{j}")
    filepath = os.getcwd() + "/journal.txt"
    PersistenceManager.save_to_file(j, filepath)

    with open(filepath, "r", encoding="UTF-8") as file:
        print(file.read())
