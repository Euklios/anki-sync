import abc
from typing import Iterable

from data.NoteDetails import NoteDetails


class BaseNoteProvider(abc.ABC):
    @abc.abstractmethod
    def list_notes(self) -> Iterable[NoteDetails]:
        pass
