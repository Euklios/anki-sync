import abc


class BaseEndpoint(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def config_class():
        pass

    @staticmethod
    @abc.abstractmethod
    def endpoint_name() -> str:
        pass
