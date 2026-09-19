import json
from django.shortcuts import render
from cities.models import City
from .models import Weather

def weather_view(request):
    cities = City.objects.all().order_by('name')
    selected_city_id = request.GET.get('city')

    selected_city = None
    if selected_city_id:
        selected_city = City.objects.filter(id=selected_city_id).first()
    if not selected_city and cities.exists():
        selected_city = cities.first()

    # Overview table for all cities
    weather_overview = []
    for c in cities:
        wt = c.latest_weather
        if wt:
            weather_overview.append({
                'city': c,
                'temp': wt.temperature,
                'humidity': wt.humidity,
                'rainfall': wt.rainfall,
                'wind_speed': wt.wind_speed,
                'pressure': wt.pressure,
                'condition': wt.condition,
                'comfort': wt.get_comfort_index(),
            })

    # Historical weather data for selected city
    chart_data = {'dates': [], 'temp': [], 'humidity': [], 'wind': [], 'rain': []}
    latest_wt = None
    if selected_city:
        latest_wt = selected_city.latest_weather
        records = selected_city.weather_records.order_by('recorded_date')[:15]
        for r in records:
            chart_data['dates'].append(r.recorded_date.strftime('%d %b'))
            chart_data['temp'].append(r.temperature)
            chart_data['humidity'].append(r.humidity)
            chart_data['wind'].append(r.wind_speed)
            chart_data['rain'].append(r.rainfall)

    context = {
        'cities': cities,
        'selected_city': selected_city,
        'latest_wt': latest_wt,
        'weather_overview': weather_overview,
        'chart_data_json': json.dumps(chart_data),
    }
    return render(request, 'weather/index.html', context)
