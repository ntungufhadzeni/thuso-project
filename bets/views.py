import datetime
from collections import defaultdict
from django.shortcuts import render
from .models import Match


def match_list(request):
    date = datetime.datetime.now().date()
    unique_countries = Match.objects.filter(time__gt=date).values_list('country', flat=True).distinct()

    filtered_matches = []
    selected_country = []
    result_list = []

    if request.method == 'POST':
        selected_country = request.POST.get('selected_country')
        if selected_country:
            filtered_matches = Match.objects.filter(time__gt=date, country=selected_country)
    elif unique_countries:
        selected_country = unique_countries[0]  # Default selection
        filtered_matches = Match.objects.filter(time__gt=date, country=selected_country)

    if filtered_matches:
        # Create a defaultdict to store matches by league
        matches_by_league = defaultdict(list)

        # Group matches by the 'league' field
        for match in filtered_matches:
            matches_by_league[match.league].append({
                'home_team': match.home_team,
                'away_team': match.away_team,
                'match_time': match.match_time,
                'bet': match.bet,
                'prob': match.prob,
                'home_team_form': match.home_team_form,
                'away_team_form': match.away_team_form,
                'home_team_pos': match.home_team_pos,
                'away_team_pos': match.away_team_pos,
            })

        # Convert the defaultdict to a list of dictionaries
        result_list = [{'league': league, 'matches': matches} for league, matches in matches_by_league.items()]

    context = {
        'unique_countries': unique_countries,
        'selected_country': selected_country,
        'result_list': result_list,
        'date': date
    }

    return render(request, 'bets/home.html', context)
