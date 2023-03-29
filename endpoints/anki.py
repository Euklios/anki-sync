import json
import typing
from typing import Iterable

import requests

from data.NoteDetails import NoteDetails
from endpoints.abc.NoteConsumer import BaseNoteConsumer
from endpoints.abc.NoteProvider import BaseNoteProvider
from utils import map_fields


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

        return notes

    def __init__(self, settings: AnkiSettings):
        self.settings = settings

    def store_note(self, note: NoteDetails) -> None:
        pass

    def update_note(self, note, query: str, content_info: NoteDetails) -> None:
        filename = f'{query}.mp3'

        self.anki_request('addTags', notes=[note['noteId']], tags=' '.join(content_info.tags))

        fields = map_fields(self.settings.field_mappings, content_info.fields)

        if content_info.pronunciation:
            self.anki_request('storeMediaFile', filename=filename, url=content_info.pronunciation)
            fields[self.settings.pronunciation_field] = f'[sound:{filename}]'
        else:
            fields[self.settings.pronunciation_field] = ''

        self.anki_request('updateNoteFields', note={
            'id': note['noteId'],
            'fields': fields
        })

    def anki_request(self, action: str, **params):
        request_payload = json.dumps({'action': action, 'params': params, 'version': 6}).encode('UTF-8')
        response = requests.request('get', self.settings.host, data=request_payload)

        if 200 > response.status_code or response.status_code >= 300:
            raise IOError("Failed to communicate with anki")

        response_json = response.json()

        if response_json['error'] is not None:
            raise IOError(f"Failed to call anki action {action}: {response_json['error']}")

        return response_json
