from typing import List

from data.NoteDetails import NoteDetails
from utils.decorators import retry
from endpoints.abc.NoteConsumer import BaseNoteConsumer
from endpoints.abc.NoteProvider import BaseNoteProvider
from endpoints.abc.BaseProvider import BaseProvider
from utils.utils import merge_details, save_or_update_note


class Step:
    def __init__(self, source: BaseNoteProvider, target: BaseNoteConsumer, enrichments: List[BaseProvider]):
        self.source = source
        self.target = target
        self.enrichments: List[BaseProvider] = enrichments

    def process_step(self):
        self.source.sync_profile()

        for note in self.source.list_notes():
            self.update_single_note(note)

        self.target.sync_profile()

    @retry(times=5, exceptions=(ConnectionError, IOError), delay=5)
    def update_single_note(self, note: NoteDetails):
        # TODO: The question field should be configurable
        query = note.fields['Question']

        for provider in self.enrichments:
            details = provider.update_content_by_query(query, note)

            note = merge_details(note, details)

        save_or_update_note(self.target, note, query)
