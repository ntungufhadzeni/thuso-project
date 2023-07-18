from django.db import models
from django.utils import timezone


class CoverLetterSubscriber(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    whatsapp_number = models.CharField(max_length=11)
    expire_date = models.DateField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
