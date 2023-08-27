import datetime
import json
import os

from celery import shared_task
from django.conf import settings
import requests
from .models import Match


@shared_task(name='get_matches_from_api')
def get_matches_api():
    headers = {
        "X-RapidAPI-Key": settings.X_RapidAPI_Key,
        "X-RapidAPI-Host": settings.X_RapidAPI_Host
    }
    response = requests.get(settings.API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        save_data(data)


@shared_task(name='get_matches_from_file')
def get_matches_file(filename):
    data = []
    # Get the  directory
    directory = os.path.join(settings.BASE_DIR, 'bets', 'files')

    # Build the file path
    file_path = os.path.join(directory, filename)

    # Check if the file exists
    if os.path.exists(file_path):
        # Load JSON content from the file
        with open(file_path, "r") as file:
            data = json.load(file)
            file.close()
    save_data(data)


@shared_task(name='save_data')
def save_data(data):
    if data:
        for entry in data:
            for game in entry['matches']:
                dt = datetime.datetime.strptime(f"{game['date_match']} {game['hour_match']}",
                                                '%Y-%m-%d %H:%M:%S') + \
                     datetime.timedelta(hours=2)
                home_team_form = ''
                away_team_form = ''
                for home_result in game['results']['home_team']:
                    home_team_form += f"{home_result['outcome']}"

                for away_result in game['results']['away_team']:
                    away_team_form += f"{away_result['outcome']}"

                home_team_pos = ''
                away_team_pos = ''

                for standing in game['standings']['standings']:
                    if 'home_team' in standing:
                        home_team_pos = standing['home_team']
                    if 'away_team' in standing:
                        away_team_pos = standing['away_team']
                match = Match(country=entry['country'],
                              league=entry['league'],
                              home_team=game['home_team'],
                              away_team=game['away_team'],
                              time=dt,
                              bet=game['bet'],
                              prob=game['prob'],
                              home_team_form=home_team_form,
                              away_team_form=away_team_form,
                              home_team_pos=home_team_pos,
                              away_team_pos=away_team_pos
                              )
                match.save()
