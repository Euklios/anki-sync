import abc
from typing import Iterable

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseEndpoint import BaseEndpoint


class BaseNoteConsumer(BaseEndpoint, abc.ABC):
    @abc.abstractmethod
    def store_note(self, note: NoteDetails) -> None:
        pass

    @abc.abstractmethod
    def update_note(self, note, query: str, content_info: NoteDetails) -> None:
        pass

    def sync_profile(self):
        pass
