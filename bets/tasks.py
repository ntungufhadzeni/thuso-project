import datetime

import requests
from celery import shared_task
from django.conf import settings

from .models import Match


@shared_task(name='get_matches_from_api')
def get_matches_api():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    params = {"market": "classic", "iso_date": date, "federation": "UEFA"}
    headers = {
        "X-RapidAPI-Key": settings.X_RAPIDAPI_KEY,
        "X-RapidAPI-Host": settings.X_RAPIDAPI_HOST
    }
    response = requests.get(settings.API_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()['data']
        save_data(data)


@shared_task(name='save_data')
def save_data(data):
    if data:
        for entry in data:
            start_date = datetime.datetime.strptime(entry['start_date'], '%Y-%m-%dT%H:%M:%S') + datetime.timedelta(
                hours=1)
            match = Match(
                id=entry['id'],
                country=entry['competition_cluster'],
                competition=entry['competition_name'],
                federation=entry['federation'],
                home_team=entry['home_team'],
                away_team=entry['away_team'],
                start_date=start_date,
                bet=entry['prediction'],
                result=entry['result'],
                status=entry['status']
            )
            match.save()
