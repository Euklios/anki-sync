import abc

from data.NoteDetails import NoteDetails
from endpoints.abc.BaseProvider import BaseProvider


class SplitManipulationConfig:
    source_field: str = None
    search_string: str = None
    target_field_left: str = None
    target_field_right: str = None


class SplitManipulation(BaseProvider):
    def __init__(self, settings: SplitManipulationConfig):
        self.settings = settings

    def update_content_by_query(self, query: str, existing_details: NoteDetails) -> NoteDetails:
        data = existing_details.fields[self.settings.source_field]
        details = NoteDetails()

        try:
            [left, right] = data.split(self.settings.search_string, 2)
        except ValueError:
            return details

        details.fields[self.settings.target_field_left] = left
        details.fields[self.settings.target_field_right] = right

        return details

    @staticmethod
    def config_class():
        return SplitManipulationConfig

    @staticmethod
    def endpoint_name() -> str:
        return "split"


class ReplacementConfig:
    source_field: str = None
    target_field: str = None
    search_string: str = ""
    replacement_string: str = ""


class GenericReplacement(BaseProvider, abc.ABC):
    def __init__(self, settings: ReplacementConfig):
        self.settings = settings

    def update_content_by_query(self, query: str, existing_details: NoteDetails) -> NoteDetails:
        target = NoteDetails()

        source_field = self.settings.source_field
        target_field = self.settings.target_field if self.settings.target_field else source_field

        data = existing_details.fields[source_field]
        updated = self._apply_replacement(data, self.settings.search_string, self.settings.replacement_string)
        target.fields[target_field] = updated

        return target

    @staticmethod
    def config_class():
        return ReplacementConfig

    @abc.abstractmethod
    def _apply_replacement(self, data: str, search: str, replace: str) -> str:
        pass


class ReplacePrefix(GenericReplacement):
    def _apply_replacement(self, data: str, search: str, replace: str) -> str:
        if data.startswith(search):
            return replace + data.removeprefix(search)

        return data

    @staticmethod
    def endpoint_name() -> str:
        return "replace_prefix"


class ReplaceSuffix(GenericReplacement):
    def _apply_replacement(self, data: str, search: str, replace: str) -> str:
        if data.endswith(search):
            return data.removesuffix(search) + replace

        return data

    @staticmethod
    def endpoint_name() -> str:
        return "replace_suffix"


class ReplaceInContent(GenericReplacement):
    def _apply_replacement(self, data: str, search: str, replace: str) -> str:
        return data.replace(search, replace)

    @staticmethod
    def endpoint_name() -> str:
        return "replace"
