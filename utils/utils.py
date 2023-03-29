from data.NoteDetails import NoteDetails
from endpoints.abc.NoteConsumer import BaseNoteConsumer


def map_fields(field_mappings, data):
    return {field_mappings.get(k, k): v for k, v in data.items()}


def merge_details(original: NoteDetails, updates: NoteDetails) -> NoteDetails:
    merged = NoteDetails()
    merged.source = original.source

    merged.pronunciation = updates.pronunciation if updates.pronunciation is not None else original.pronunciation
    merged.tags.update(original.tags)
    merged.tags.update(updates.tags)

    for key in original.fields:
        merged.fields[key] = original.fields[key]

    for key in updates.fields:
        merged.fields[key] = updates.fields[key]

    return merged


def _update_note(target: BaseNoteConsumer, note: NoteDetails, query: str):
    target.update_note(note, query)


def _save_note(target: BaseNoteConsumer, note: NoteDetails, query: str):
    raise "Error, new notes are currently not supported"


def save_or_update_note(target: BaseNoteConsumer, note: NoteDetails, query: str):
    if note.source is None or note.source.endpoint is not target.endpoint_name():
        _save_note(target, note, query)
    else:
        _update_note(target, note, query)
