from typing import Set, Dict, Optional


class NoteDetails:
    tags: Set[str]
    fields: Dict[str, str]
    pronunciation: Optional[str]

    def __init__(self):
        self.tags = set()
        self.fields = dict()
        self.pronunciation = None
