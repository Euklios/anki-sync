import typing
from typing import Iterable

import requests

from data.NoteDetails import NoteDetails, NoteSource
from endpoints.abc.BaseProvider import BaseProvider
from endpoints.abc.NoteProvider import BaseNoteProvider


class WanikaniSettings:
    api_token: str = None


class Wanikani(BaseProvider, BaseNoteProvider):
    def list_notes(self) -> Iterable[NoteDetails]:
        assignments = list(self._load_assignments())

        for assignment in assignments:
            subject = list(filter(lambda e: e['id'] == assignment['data']['subject_id'], self.subjects))[0]

            yield self._convert_subject_to_note_details(subject)

    @staticmethod
    def config_class() -> typing.Type:
        return WanikaniSettings

    @staticmethod
    def endpoint_name() -> str:
        return "wanikani"

    api_base = "https://api.wanikani.com/v2/"

    def __init__(self, settings: WanikaniSettings):
        self.token = settings.api_token
        self.subjects = list(self._load_subjects())

    def _get(self, path):
        response = requests.get(f"{self.api_base}{path}", headers={"Authorization": f"Bearer {self.token}"})

        if not 200 <= response.status_code < 300:
            raise IOError(f"Failed to load resource {path}. [{response.status_code}]: {response.text}")

        return response.json()

    def _load_assignments(self):
        next_path = "assignments?subject_types=vocabulary&started=true"

        while True:
            response = self._get(next_path)
            yield from response['data']

            if response['pages']['next_url'] is None:
                return

            # TODO: This will most likely fail. The base path needs to be removed first
            next_path = response['pages']['next_url']

    def _load_subjects(self):
        total_count = 1
        collected_count = 0
        next_path = "subjects"

        while total_count > collected_count:
            response = self._get(next_path)
            yield from response['data']

            if response['pages']['next_url'] is None:
                return

            next_path = f'subjects?{response["pages"]["next_url"].split("?", 1)[1]}'
            total_count = response['total_count']
            collected_count += len(response['data'])

    def search_content_by_string(self, query: str) -> NoteDetails:
        details = NoteDetails()
        try:
            vocab = next(filter(lambda a: a['data']['characters'] == query and a['object'] == 'vocabulary', self.subjects))
        except StopIteration:
            return details

        details.source = NoteSource(self.endpoint_name(), vocab['id'])

        details.fields['meaning_mnemonic'] = vocab['data']['meaning_mnemonic']
        details.fields['reading_mnemonic'] = vocab['data']['reading_mnemonic']
        details.tags.add(f"wanikani{vocab['data']['level']}")
        details.pronunciation = vocab['data']['pronunciation_audios'][0]['url']

        return details

    def _convert_subject_to_note_details(self, subject) -> NoteDetails:
        details = NoteDetails()
        details.source = NoteSource(self.endpoint_name(), subject['id'])

        details.fields['Question'] = subject['data']['slug']
        details.fields['Answer'] = ", ".join([meaning['meaning'] for meaning in subject['data']['meanings'] if meaning['accepted_answer']])
        details.fields['meaning_mnemonic'] = subject['data']['meaning_mnemonic']
        details.fields['reading_mnemonic'] = subject['data']['reading_mnemonic']
        details.tags.add(f"wanikani{subject['data']['level']}")
        details.pronunciation = subject['data']['pronunciation_audios'][0]['url']

        return details
