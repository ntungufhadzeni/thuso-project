from abc import ABC, abstractmethod
from cover_letter.models import CoverLetterSubscriber
from cover_letter.schemas.subscriber import Subscriber


class AbstractSubscriberRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, pk):
        raise NotImplementedError

    @abstractmethod
    def create(self, obj: CoverLetterSubscriber):
        raise NotImplementedError

    @abstractmethod
    def delete(self, pk):
        raise NotImplementedError


class SubscriberRepository(AbstractSubscriberRepository):

    def get_all(self):
        return CoverLetterSubscriber.objects.all()

    def get_by_id(self, pk):
        return CoverLetterSubscriber.objects.get(pk)

    def create(self, obj: Subscriber):
        return CoverLetterSubscriber.objects.get_or_create(Subscriber.__dict__)

    def delete(self, pk):
        return CoverLetterSubscriber.objects.filter(id=pk).delete()
