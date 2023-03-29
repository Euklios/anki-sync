import abc

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseEndpoint import BaseEndpoint


class BaseNoteConsumer(BaseEndpoint, abc.ABC):
    @abc.abstractmethod
    def store_note(self, note: NoteDetails) -> None:
        pass

    @abc.abstractmethod
    def update_note(self, note: NoteDetails, query: str) -> None:
        pass

    def sync_profile(self):
        pass
