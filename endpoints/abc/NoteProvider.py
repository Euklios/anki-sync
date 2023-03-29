import abc
from typing import Iterable

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseEndpoint import BaseEndpoint


class BaseNoteProvider(BaseEndpoint, abc.ABC):
    @abc.abstractmethod
    def list_notes(self) -> Iterable[NoteDetails]:
        pass
