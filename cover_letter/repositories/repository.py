from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk):
        raise NotImplementedError

    @abstractmethod
    def create(self, data):
        raise NotImplementedError

    @abstractmethod
    def update(self, pk, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk):
        raise NotImplementedError
