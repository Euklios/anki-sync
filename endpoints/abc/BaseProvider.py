import abc

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseEndpoint import BaseEndpoint


class BaseProvider(BaseEndpoint, abc.ABC):
    @abc.abstractmethod
    def update_content_by_query(self, query: str, existing_details: NoteDetails) -> NoteDetails:
        pass
