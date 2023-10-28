from cover_letter.models import CoverLetterSubscriber
from cover_letter.repositories.repository import AbstractRepository
from cover_letter.schemas.subscriber_model import SubscriberModel


class SubscriberSQLRepository(AbstractRepository):

    def get_all(self):
        return CoverLetterSubscriber.objects.all()

    def get_by_id(self, pk):
        return CoverLetterSubscriber.objects.get(pk)

    def update(self, pk, data):
        return CoverLetterSubscriber.objects.get_or_create(**data.dict())

    def create(self, data: SubscriberModel):
        return CoverLetterSubscriber.objects.get_or_create(**data.dict())

    def delete(self, pk):
        return CoverLetterSubscriber.objects.filter(id=pk).delete()
