from pydantic_redis import RedisConfig, Store
from .schemas import CoverLetter
from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk):
        raise NotImplementedError

    @abstractmethod
    def create(self, pk):
        raise NotImplementedError

    @abstractmethod
    def update(self, pk, data):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk):
        raise NotImplementedError


class AnswerRepository(IRepository):
    store = Store(name='some_name', redis_config=RedisConfig(db=5, host='redis', port=6379),
                  life_span_in_seconds=3600)
    store.register_model(CoverLetter)

    def get_all(self):
        return CoverLetter.select()

    def get_by_id(self, pk):
        return CoverLetter.select(ids=[pk])

    def create(self, pk):
        CoverLetter.insert([CoverLetter(whatsapp_number=pk)])
        return CoverLetter.select(ids=[pk])

    def update(self, pk, data: dict):
        CoverLetter.update(_id=pk, data=data)
        return CoverLetter.select(ids=[pk])

    def delete(self, pk: str):
        CoverLetter.delete(ids=[pk])

