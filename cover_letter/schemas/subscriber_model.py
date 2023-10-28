from pydantic_redis import Model


class SubscriberModel(Model):
    whatsapp_name: str
    whatsapp_number: str
