import re
from typing import List

from data.NoteDetails import NoteDetails
from utils.decorators import retry
from endpoints.abc.NoteConsumer import BaseNoteConsumer
from endpoints.abc.NoteProvider import BaseNoteProvider
from endpoints.abc.BaseProvider import BaseProvider


def cleanup_query(question):
    question = re.compile('<rt>[^<]*</rt>').sub('', question)
    question = question.replace('<ruby>', '').replace('</ruby>', '')

    return question


class Step:
    def __init__(self, source: BaseNoteProvider, target: BaseNoteConsumer, enrichments: List[BaseProvider]):
        self.source = source
        self.target = target
        self.enrichments: List[BaseProvider] = enrichments

    def process_step(self):
        for note in self.source.list_notes():
            self.update_single_note(note)

    @retry(times=5, exceptions=(ConnectionError, IOError), delay=5)
    def update_single_note(self, note):
        # TODO: The question field should be configurable
        # TODO: cleanup_query should be removed
        query = cleanup_query(note['fields']['Question']['value'])

        details = NoteDetails()
        for provider in self.enrichments[::-1]:
            provider.search_content_by_string(query, details)

        self.target.update_note(note, query, details)
