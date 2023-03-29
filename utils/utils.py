from data.NoteDetails import NoteDetails


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
