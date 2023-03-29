import abc

from data.NoteDetails import NoteDetails


class BaseProvider(abc.ABC):
    @abc.abstractmethod
    def search_content_by_string(self, query: str, details: NoteDetails) -> None:
        pass
