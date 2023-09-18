import datetime
from collections import defaultdict
from django.shortcuts import render
from .models import Match


def match_list(request):
    date = datetime.datetime.now().date()
    unique_countries = Match.objects.filter(start_date__date=date)\
        .order_by('country').values_list('country', flat=True).distinct()

    filtered_matches = []
    selected_country = []
    result_list = []

    if request.method == 'POST':
        selected_country = request.POST.get('selected_country')
        picked_date = request.POST.get('selected_date')
        date = datetime.datetime.strptime(picked_date, '%Y-%m-%d').date()
        if selected_country:
            filtered_matches = Match.objects.filter(start_date__date=date, country=selected_country)
            unique_countries = Match.objects.filter(start_date__date=date) \
                .order_by('country').values_list('country', flat=True).distinct()
    elif unique_countries:
        selected_country = unique_countries[0]  # Default selection
        filtered_matches = Match.objects.filter(start_date__date=date, country=selected_country)

    if filtered_matches:
        # Create a defaultdict to store matches by league
        matches_by_league = defaultdict(list)

        # Group matches by the 'league' field
        for match in filtered_matches:
            matches_by_league[match.competition].append({
                'home_team': match.home_team,
                'away_team': match.away_team,
                'start_date': match.start_date,
                'prediction': match.prediction,
                'result': match.result,
                'status': match.status,
            })

        # Convert the defaultdict to a list of dictionaries
        result_list = [{'competition': league, 'matches': matches} for league, matches in matches_by_league.items()]

    context = {
        'unique_countries': unique_countries,
        'selected_country': selected_country,
        'result_list': result_list,
        'date': date
    }

    return render(request, 'bets/home.html', context)
