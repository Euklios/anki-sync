import typing
from typing import Iterable

from jisho_api.word import Word
from jisho_api.word.cfg import WordConfig
from jisho_api.word.request import WordRequest
from tqdm import tqdm

from endpoints.abc.BaseProvider import BaseProvider
from data.NoteDetails import NoteDetails


class JishoSettings:
    common_only: bool = True


class Jisho(BaseProvider):
    @staticmethod
    def config_class() -> typing.Type:
        return JishoSettings

    @staticmethod
    def endpoint_name() -> str:
        return "jisho"

    def __init__(self, settings: JishoSettings):
        self.api_client = Word()
        self.common_only = settings.common_only

    def update_content_by_query(self, query: str, existing_details: NoteDetails) -> NoteDetails:
        details = NoteDetails()
        matches = list(self._filter_matches(self.api_client.request(query), query))

        if len(matches) == 0:
            return details

        if len(matches) > 1:
            tqdm.write(f"No unique match found for query {query}")
            return details

        match = matches[0]

        details.tags.update(match.tags)
        details.tags.update(match.jlpt)

        return details

    def _filter_matches(self, data: WordRequest, query: str) -> Iterable[WordConfig]:
        if data is None:
            return

        for entry in data.data:
            if self.common_only and not entry.is_common:
                continue

            if entry.slug == query:
                yield entry
                continue

            for japanese_definition in entry.japanese:
                if japanese_definition.reading == query or japanese_definition.word == query:
                    yield entry
                    break
