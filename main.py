import re

from anki import anki_request, update_anki_note
from data.NoteDetails import NoteDetails
from data.Settings import Settings
from decorators import retry
from providers.jisho import Jisho
from providers.wani import Wanikani
from tqdm import tqdm

from settings_loader import load_settings

FIELD_MAPPINGS = {
    'meaning_mnemonic': 'Meaning Mnemonic',
    'reading_mnemonic': 'Reading Mnemonic'
}


# TODO: Revert back to list, this should not instantiate the providers
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

    notes = anki_request(settings, 'findNotes', query=f'deck:{settings.anki.target_deck}')['result']
    notes = anki_request(settings, 'notesInfo', notes=notes)

    for note in tqdm(notes['result']):
        update_single_note(note, settings)


@retry(times=5, exceptions=(ConnectionError, IOError), delay=5)
def update_single_note(note, settings: Settings):
    query = cleanup_query(note['fields'][settings.anki.question_field]['value'])
    details = NoteDetails()
    for provider in get_providers(settings=settings)[::-1]:
        provider.search_content_by_string(query, details)
    update_anki_note(settings, note, query, details)


if __name__ == '__main__':
    main()
