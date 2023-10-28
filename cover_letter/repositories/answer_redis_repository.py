from cover_letter.repositories.repository import AbstractRepository
from cover_letter.schemas.answer_model import AnswerModel
from pydantic_redis import RedisConfig, Store
from typing import List


class AnswerRedisRepository(AbstractRepository):
    store = Store(name='answers', redis_config=RedisConfig(db=5, host='redis', port=6379),
                  life_span_in_seconds=3600)
    store.register_model(AnswerModel)

    def get_all(self):
        return AnswerModel.select()

    def get_by_id(self, pk) -> List[AnswerModel]:
        return AnswerModel.select(ids=[pk])

    def update(self, pk: str, data: dict):
        return AnswerModel.update(_id=pk, data=data, life_span_seconds=3600)

    def create(self, data: AnswerModel):
        AnswerModel.insert([data], life_span_seconds=3600)
        return AnswerModel.select(ids=[data.whatsapp_number])

    def delete(self, pk: str):
        return AnswerModel.delete(ids=[pk])
