import datetime

from django.shortcuts import render
from .models import Match


def match_list(request):
    date = datetime.datetime.now().date()
    unique_countries = Match.objects.filter(time__gt=date).values_list('country', flat=True).distinct()

    filtered_matches = []
    selected_country = []

    if request.method == 'POST':
        selected_country = request.POST.get('selected_country')
        if selected_country:
            filtered_matches = Match.objects.filter(time__gt=date, country=selected_country)
    elif unique_countries:
        selected_country = unique_countries[0]  # Default selection
        filtered_matches = Match.objects.filter(time__gt=date, country=selected_country)

    context = {
        'unique_countries': unique_countries,
        'selected_country': selected_country,
        'filtered_matches': filtered_matches,
        'date': date
    }

    return render(request, 'bets/home.html', context)
