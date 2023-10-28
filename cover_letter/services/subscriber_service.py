from cover_letter.repositories.repository import AbstractRepository


class SubscriberService:
    def __init__(self, repository: AbstractRepository):
        self.__repository = repository

    def create(self, data):
        return self.__repository.create(data)

    def get_all(self):
        return self.__repository.get_all()
