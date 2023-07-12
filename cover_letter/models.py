from django.db import models
from django.utils import timezone
from uuid import uuid4

class CoverLetter(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=200)
    hiring_manager = models.CharField(max_length=100, blank=True)
    introduction = models.TextField()
    skills_and_qualifications = models.TextField()
    achievements = models.TextField()
    motivation = models.TextField()
    closing = models.TextField()
    
    uniqueId = models.CharField(null=True, blank=True, unique=True, max_length=100)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]

        self.last_updated = timezone.localtime(timezone.now())
        super(CoverLetter, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name
    
    

