import re
from typing import List

from data.NoteDetails import NoteDetails
from data.Settings import Settings
from decorators import retry
from endpoints.abc.BaseProvider import BaseProvider
from endpoints.anki import Anki
from endpoints.jisho import Jisho
from endpoints.wani import Wanikani
from tqdm import tqdm

from settings_loader import load_settings

FIELD_MAPPINGS = {
    'meaning_mnemonic': 'Meaning Mnemonic',
    'reading_mnemonic': 'Reading Mnemonic'
}


# TODO: Revert back to list, this should not instantiate the endpoints
def get_providers(settings: Settings):
    return [
        Wanikani(settings.wanikani.api_token),
        Jisho(common_only=True)
    ]


def cleanup_query(question):
    question = re.compile('<rt>[^<]*</rt>').sub('', question)
    question = question.replace('<ruby>', '').replace('</ruby>', '')

    return question


def main():
    settings = load_settings()

    anki = Anki(settings.anki)
    providers = get_providers(settings)

    for note in tqdm(anki.list_notes()):
        update_single_note(note, settings, providers, anki)


@retry(times=5, exceptions=(ConnectionError, IOError), delay=5)
def update_single_note(note, settings: Settings, providers: List[BaseProvider], anki: Anki):
    query = cleanup_query(note['fields'][settings.anki.question_field]['value'])

    details = NoteDetails()
    for provider in providers[::-1]:
        provider.search_content_by_string(query, details)

    anki.update_note(note, query, details)


if __name__ == '__main__':
    main()
