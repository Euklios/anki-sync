import abc
from typing import Iterable

from data.NoteDetails import NoteDetails


class BaseNoteConsumer(abc.ABC):
    @abc.abstractmethod
    def store_note(self, note: NoteDetails) -> None:
        pass

    @abc.abstractmethod
    def update_note(self, note, query: str, content_info: NoteDetails) -> None:
        pass
