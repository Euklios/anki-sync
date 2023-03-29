from typing import Set, Dict, Optional


class NoteSource:
    endpoint: str
    identifier: str

    def __init__(self, endpoint: str, identifier: str):
        self.endpoint = endpoint
        self.identifier = identifier


class NoteDetails:
    tags: Set[str]
    fields: Dict[str, str]
    pronunciation: Optional[str]

    source: Optional[NoteSource]

    def __init__(self):
        self.tags = set()
        self.fields = dict()
        self.pronunciation = None
