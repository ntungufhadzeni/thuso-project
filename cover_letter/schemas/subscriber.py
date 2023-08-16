from pydantic_redis import Model


class Subscriber(Model):
    whatsapp_name: str
    whatsapp_number: str
    whatsapp_id: str
