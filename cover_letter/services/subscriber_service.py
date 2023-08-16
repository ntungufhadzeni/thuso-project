from cover_letter.repositories.subscriber_repository import SubscriberRepository


class SubscriberService:
    def __init__(self):
        self.repo = SubscriberRepository()

    def create(self, obj):
        return self.repo.create(obj)

    def get_all(self):
        return self.repo.get_all()