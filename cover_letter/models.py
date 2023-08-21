import uuid

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, max_length=34)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class CoverLetterSubscriber(TimeStampedModel):
    whatsapp_name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.whatsapp_name}'
