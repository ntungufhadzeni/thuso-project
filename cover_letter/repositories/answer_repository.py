from abc import ABC, abstractmethod
from cover_letter.schemas.answer import Answer
from pydantic_redis import RedisConfig, Store


class AbstractAnswerRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk):
        raise NotImplementedError

    @abstractmethod
    def insert(self, obj: Answer):
        raise NotImplementedError

    @abstractmethod
    def update(self, pk: str, data: dict):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk: str):
        raise NotImplementedError


class AnswerRepository(AbstractAnswerRepository):
    store = Store(name='answers', redis_config=RedisConfig(db=5, host='redis', port=6379),
                  life_span_in_seconds=3600)
    store.register_model(Answer)

    def get_all(self):
        return Answer.select()

    def get_by_id(self, pk):
        return Answer.select(ids=[pk])

    def update(self, pk: str, data: dict):
        return Answer.update(_id=pk, data=data, life_span_seconds=3600)

    def insert(self, obj: Answer):
        Answer.insert([obj], life_span_seconds=3600)
        return Answer.select(ids=[obj.whatsapp_number])

    def delete(self, pk: str):
        return Answer.delete(ids=[pk])
