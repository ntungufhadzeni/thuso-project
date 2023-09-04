from django.db import models
from django.utils import timezone
import uuid


class Match(models.Model):
    id = models.IntegerField(editable=False, primary_key=True)
    created_at = models.DateTimeField(default=timezone.now)
    country = models.CharField(max_length=50)
    federation = models.CharField(max_length=50)
    competition = models.CharField(max_length=50)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    bet = models.CharField(max_length=2)
    status = models.CharField(max_length=20)
    result = models.CharField(max_length=10)
    start_date = models.DateTimeField()
    last_update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team} ({self.start_date.strftime('%B %d, %Y %H:%M')})"

    @property
    def prediction(self):
        if self.bet == '1':
            return 'Home team win'
        elif self.bet == 'X':
            return 'Draw'
        elif self.bet == '2':
            return 'Away team win'
        elif self.bet == '1X':
            return 'Home team or draw'
        elif self.bet == 'X2':
            return 'Away team or draw'
        elif self.bet == '12':
            return 'Home team or away team'
        else:
            return self.bet


