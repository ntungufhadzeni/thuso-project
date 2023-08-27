from django.db import models
from django.utils import timezone
import uuid


class Match(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=50, blank=True)
    league = models.CharField(max_length=50)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    time = models.DateTimeField()
    bet = models.CharField(max_length=50)
    prob = models.CharField(max_length=2)
    home_team_form = models.CharField(max_length=10)
    away_team_form = models.CharField(max_length=10)
    home_team_pos = models.CharField(max_length=50)
    away_team_pos = models.CharField(max_length=50)

    @property
    def match_date(self):
        return self.time.strftime('%d/%m/%Y')

    @property
    def match_time(self):
        return f"{self.time.strftime('%H:%M')} (CAT)"
