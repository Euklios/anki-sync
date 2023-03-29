import abc
import typing


class BaseEndpoint(abc.ABC):
    @abc.abstractmethod
    def config_class(self) -> typing.Type:
        pass

    @abc.abstractmethod
    def endpoint_name(self) -> str:
        pass
