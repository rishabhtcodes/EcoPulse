import json
from django.shortcuts import render
from django.db.models import Avg, Max, Min
from cities.models import City
from .models import AirQuality, EnvironmentalAnalysis

def analytics_view(request):
    selected_city_id = request.GET.get('city')
    cities = City.objects.all().order_by('name')

    selected_city = None
    if selected_city_id:
        selected_city = City.objects.filter(id=selected_city_id).first()
    if not selected_city and cities.exists():
        selected_city = cities.first()

    # Ranking table across all cities
    rankings = []
    for c in cities:
        aq = c.latest_air_quality
        if aq:
            rankings.append({
                'city': c,
                'aqi': aq.aqi,
                'pm25': aq.pm25,
                'pm10': aq.pm10,
                'no2': aq.no2,
                'so2': aq.so2,
                'co': aq.co,
                'o3': aq.o3,
                'dominant': aq.get_dominant_pollutant(),
                'risk_level': aq.get_risk_level(),
                'risk_color': aq.get_risk_color(),
                'traffic': aq.traffic_level,
                'score': aq.calculate_environmental_score(),
            })
    rankings.sort(key=lambda x: x['aqi'], reverse=True)

    # City specific historical breakdown
    selected_history = []
    chart_data = {'dates': [], 'pm25': [], 'pm10': [], 'no2': [], 'so2': [], 'aqi': []}
    percentages = {}

    if selected_city:
        records = selected_city.air_quality_records.order_by('recorded_date')[:15]
        latest_aq = selected_city.latest_air_quality
        if latest_aq:
            percentages = latest_aq.get_pollutant_percentages()

        for r in records:
            chart_data['dates'].append(r.recorded_date.strftime('%d %b'))
            chart_data['aqi'].append(r.aqi)
            chart_data['pm25'].append(r.pm25)
            chart_data['pm10'].append(r.pm10)
            chart_data['no2'].append(r.no2)
            chart_data['so2'].append(r.so2)

    # Top Polluted and Cleanest
    most_polluted = rankings[0] if rankings else None
    cleanest = rankings[-1] if rankings else None
    avg_aqi = round(sum(r['aqi'] for r in rankings) / len(rankings), 1) if rankings else 0

    context = {
        'cities': cities,
        'selected_city': selected_city,
        'rankings': rankings,
        'most_polluted': most_polluted,
        'cleanest': cleanest,
        'avg_aqi': avg_aqi,
        'percentages': percentages,
        'percentages_json': json.dumps(percentages),
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'pollution/analytics.html', context)
