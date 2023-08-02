from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    id = models.UUIDField(max_length=34, primary_key=True)

    class Meta:
        abstract = True


class CoverLetterSubscriber(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    whatsapp_number = models.CharField(max_length=11)
    expire_date = models.DateField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
