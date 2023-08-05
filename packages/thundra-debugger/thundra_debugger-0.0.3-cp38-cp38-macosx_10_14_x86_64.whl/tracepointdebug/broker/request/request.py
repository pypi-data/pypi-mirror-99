import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Request(ABC):

    @abc.abstractmethod
    def get_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_client(self):
        pass
