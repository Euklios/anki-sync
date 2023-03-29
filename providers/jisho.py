from typing import Iterable

from jisho_api.word import Word
from jisho_api.word.cfg import WordConfig
from jisho_api.word.request import WordRequest
from tqdm import tqdm

from data.BaseProvider import BaseProvider
from data.NoteDetails import NoteDetails


class Jisho(BaseProvider):
    def __init__(self, common_only=True):
        self.api_client = Word()
        self.common_only = common_only

    def search_content_by_string(self, query: str, detail: NoteDetails) -> None:
        matches = list(self._filter_matches(self.api_client.request(query), query))

        if len(matches) == 0:
            return

        if len(matches) > 1:
            tqdm.write(f"No unique match found for query {query}")
            return

        match = matches[0]

        detail.tags.update(match.tags)
        detail.tags.update(match.jlpt)

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
