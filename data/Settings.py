from typing import Dict


class WanikaniSettings:
    api_token: str = None


class AnkiSettings:
    host: str = "http://localhost:8765/"
    target_deck: str = None
    question_field: str = "Question"
    pronunciation_field: str = 'Pronunciation'
    field_mappings: Dict[str, str] = {
        'meaning_mnemonic': 'Meaning Mnemonic',
        'reading_mnemonic': 'Reading Mnemonic'
    }


class Settings:
    wanikani = WanikaniSettings()
    anki = AnkiSettings()
