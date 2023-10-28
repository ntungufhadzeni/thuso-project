from pydantic_redis import Model


class AnswerModel(Model):
    _primary_key_field: str = 'whatsapp_number'
    whatsapp_number: str
    full_name: str | None
    phone_number: str | None
    address: str | None
    email: str | None
    job_title: str | None
    company_name: str | None
    company_address: str | None
    hiring_manager: str | None
    introduction: str | None
    skills_and_qualifications: str | None
    achievements: str | None
    motivation: str | None
    closing: str | None

    def __str__(self):
        return self.full_name
