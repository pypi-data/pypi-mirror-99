import abc

ABC = abc.ABCMeta('ABC', (object,), {})


class Response(ABC):

    @abc.abstractmethod
    def get_request_id(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass

    @abc.abstractmethod
    def get_client(self):
        pass

    def get_type(self):
        return "Response"

    @abc.abstractmethod
    def is_erroneous(self):
        pass

    @abc.abstractmethod
    def get_error_code(self):
        pass

    @abc.abstractmethod
    def get_error_type(self):
        pass
