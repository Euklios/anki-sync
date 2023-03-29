import json
import typing
from typing import Iterable

import requests

from data.NoteDetails import NoteDetails, NoteSource
from endpoints.abc.NoteConsumer import BaseNoteConsumer
from endpoints.abc.NoteProvider import BaseNoteProvider
from utils.utils import map_fields


class AnkiSettings:
    host: str = "http://localhost:8765/"
    target_deck: str = None
    question_field: str = "Question"
    pronunciation_field: str = 'Pronunciation'
    field_mappings: typing.Dict[str, str] = {
        'meaning_mnemonic': 'Meaning Mnemonic',
        'reading_mnemonic': 'Reading Mnemonic'
    }


class Anki(BaseNoteConsumer, BaseNoteProvider):
    @staticmethod
    def config_class() -> typing.Type:
        return AnkiSettings

    @staticmethod
    def endpoint_name() -> str:
        return "anki"

    def list_notes(self) -> Iterable[NoteDetails]:
        notes = self.anki_request('findNotes', query=f'deck:{self.settings.target_deck}')['result']
        notes = self.anki_request('notesInfo', notes=notes)['result']

        return [self._convert_to_note_details(note) for note in notes]

    def __init__(self, settings: AnkiSettings):
        self.settings = settings

    def store_note(self, note: NoteDetails, query: str) -> None:
        filename = f'{query}.mp3'
        fields = map_fields(self.settings.field_mappings, note.fields)
        tags = ' '.join(note.tags)

        if note.pronunciation:
            self.anki_request('storeMediaFile', filename=filename, url=note.pronunciation)
            fields[self.settings.pronunciation_field] = f'[sound:{filename}]'
        else:
            fields[self.settings.pronunciation_field] = ''

        new_note = self.anki_request(
            'addNote',
            note={
                "deckName": self.settings.target_deck,
                "modelName": "Simple Model",
                "fields": fields,
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                }
            }
        )

        self.anki_request('addTags', notes=[new_note['result']], tags=' '.join(note.tags))

    def update_note(self, note: NoteDetails, query: str) -> None:
        filename = f'{query}.mp3'

        self.anki_request('addTags', notes=[note.source.identifier], tags=' '.join(note.tags))

        fields = map_fields(self.settings.field_mappings, note.fields)

        if note.pronunciation and not note.pronunciation.startswith("[sound:"):
            self.anki_request('storeMediaFile', filename=filename, url=note.pronunciation)
            fields[self.settings.pronunciation_field] = f'[sound:{filename}]'
        else:
            fields[self.settings.pronunciation_field] = ''

        self.anki_request('updateNoteFields', note={
            'id': note.source.identifier,
            'fields': fields
        })

    def sync_profile(self):
        self.anki_request('sync')

    def anki_request(self, action: str, **params):
        request_payload = json.dumps({'action': action, 'params': params, 'version': 6}).encode('UTF-8')
        response = requests.request('get', self.settings.host, data=request_payload)

        if 200 > response.status_code or response.status_code >= 300:
            raise IOError("Failed to communicate with anki")

        response_json = response.json()

        if response_json['error'] is not None:
            raise IOError(f"Failed to call anki action {action}: {response_json['error']}")

        return response_json

    def _convert_to_note_details(self, note) -> NoteDetails:
        details = NoteDetails()
        details.tags = note['tags']
        details.fields = {key: note['fields'][key]['value'] for key in note['fields']}
        details.pronunciation = details.fields.pop(self.settings.pronunciation_field)
        details.source = NoteSource(endpoint=self.endpoint_name(), identifier=note['noteId'])

        return details
