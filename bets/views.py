from django.shortcuts import render
from .models import Match


def match_list(request):
    unique_countries = Match.objects.values_list('country', flat=True).distinct()

    filtered_matches = []
    selected_country = []

    if request.method == 'POST':
        selected_country = request.POST.get('selected_country')
        if selected_country:
            filtered_matches = Match.objects.filter(country=selected_country)
    elif unique_countries:
        selected_country = unique_countries[0]  # Default selection
        filtered_matches = Match.objects.filter(country=selected_country)

    context = {
        'unique_countries': unique_countries,
        'selected_country': selected_country,
        'filtered_matches': filtered_matches,
    }

    return render(request, 'bets/home.html', context)

