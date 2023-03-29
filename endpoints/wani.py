import typing

import requests

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseProvider import BaseProvider


class WanikaniSettings:
    api_token: str = None


class Wanikani(BaseProvider):
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

    def search_content_by_string(self, query: str, details: NoteDetails) -> None:
        try:
            vocab = next(filter(lambda a: a['data']['characters'] == query and a['object'] == 'vocabulary', self.subjects))
        except StopIteration:
            return

        details.fields['meaning_mnemonic'] = vocab['data']['meaning_mnemonic']
        details.fields['reading_mnemonic'] = vocab['data']['reading_mnemonic']
        details.tags.add(f"wanikani{vocab['data']['level']}")
        details.pronunciation = vocab['data']['pronunciation_audios'][0]['url']
