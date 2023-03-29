import abc

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseEndpoint import BaseEndpoint


class BaseProvider(BaseEndpoint, abc.ABC):
    @abc.abstractmethod
    def search_content_by_string(self, query: str, details: NoteDetails) -> None:
        pass
