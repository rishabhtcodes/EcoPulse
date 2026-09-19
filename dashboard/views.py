import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from cities.models import City
from pollution.models import AirQuality, EnvironmentalAnalysis
from weather.models import Weather
from .services import sync_city_realtime_data

def index(request):
    cities = City.objects.all().order_by('name')
    selected_city_slug = request.GET.get('city')

    # Default to user default city if authenticated, else Delhi or first city
    selected_city = None
    if selected_city_slug:
        selected_city = City.objects.filter(slug=selected_city_slug).first()
    
    if not selected_city and request.user.is_authenticated:
        if hasattr(request.user, 'profile') and request.user.profile.default_city:
            selected_city = request.user.profile.default_city
            
    if not selected_city:
        selected_city = City.objects.filter(name='Delhi').first() or cities.first()

    # Get latest data for selected city
    latest_aq = selected_city.latest_air_quality if selected_city else None
    latest_wt = selected_city.latest_weather if selected_city else None
    latest_an = selected_city.latest_analysis if selected_city else None

    # Calculate trends compared to yesterday
    yesterday_aq = None
    yesterday_wt = None
    aqi_trend = {'diff': 0, 'percent': 0, 'direction': 'neutral'}
    pm25_trend = {'diff': 0, 'percent': 0, 'direction': 'neutral'}
    temp_trend = {'diff': 0, 'percent': 0, 'direction': 'neutral'}

    if selected_city and latest_aq:
        history = list(selected_city.air_quality_records.order_by('-recorded_date')[:2])
        if len(history) > 1:
            yesterday_aq = history[1]
            diff_aqi = latest_aq.aqi - yesterday_aq.aqi
            pct_aqi = round((diff_aqi / (yesterday_aq.aqi or 1)) * 100, 1)
            aqi_trend = {
                'diff': abs(diff_aqi),
                'percent': abs(pct_aqi),
                'direction': 'up' if diff_aqi > 0 else ('down' if diff_aqi < 0 else 'neutral'),
                'is_worse': diff_aqi > 0
            }

            diff_pm = round(latest_aq.pm25 - yesterday_aq.pm25, 1)
            pct_pm = round((diff_pm / (yesterday_aq.pm25 or 1)) * 100, 1)
            pm25_trend = {
                'diff': abs(diff_pm),
                'percent': abs(pct_pm),
                'direction': 'up' if diff_pm > 0 else ('down' if diff_pm < 0 else 'neutral'),
                'is_worse': diff_pm > 0
            }

    if selected_city and latest_wt:
        wt_history = list(selected_city.weather_records.order_by('-recorded_date')[:2])
        if len(wt_history) > 1:
            yesterday_wt = wt_history[1]
            diff_temp = round(latest_wt.temperature - yesterday_wt.temperature, 1)
            temp_trend = {
                'diff': abs(diff_temp),
                'direction': 'up' if diff_temp > 0 else ('down' if diff_temp < 0 else 'neutral')
            }

    # Dynamic Pollutant composition
    pollutant_percentages = latest_aq.get_pollutant_percentages() if latest_aq else {}

    # Historical trends for line chart
    history_records = selected_city.air_quality_records.order_by('recorded_date')[:15] if selected_city else []
    history_weather = selected_city.weather_records.order_by('recorded_date')[:15] if selected_city else []

    trend_dates = [r.recorded_date.strftime('%d %b') for r in history_records]
    trend_aqi = [r.aqi for r in history_records]
    trend_pm25 = [r.pm25 for r in history_records]
    trend_pm10 = [r.pm10 for r in history_records]
    trend_temp = [r.temperature for r in history_weather]
    trend_humidity = [r.humidity for r in history_weather]

    trend_data = {
        'dates': trend_dates,
        'aqi': trend_aqi,
        'pm25': trend_pm25,
        'pm10': trend_pm10,
        'temp': trend_temp,
        'humidity': trend_humidity,
    }

    # Geospatial map points and regional breakdown matching reference design
    city_map_points = []
    top_risk_regions = []
    risk_tier_counts = {'Critical': 0, 'High': 0, 'Moderate': 0, 'Satisfactory': 0, 'Good': 0}

    # Bounds for India geographic coordinates projection onto the map canvas
    # min_lat: ~8.0, max_lat: ~36.0, min_lng: ~68.0, max_lng: ~94.0
    for c in cities:
        aq = c.latest_air_quality
        wt = c.latest_weather
        an = c.latest_analysis
        
        aqi_val = aq.aqi if aq else 100
        risk_lvl = an.risk_level if an else 'Moderate'
        if aqi_val > 300:
            risk_tier_counts['Critical'] += 1
        elif aqi_val > 200:
            risk_tier_counts['High'] += 1
        elif aqi_val > 100:
            risk_tier_counts['Moderate'] += 1
        elif aqi_val > 50:
            risk_tier_counts['Satisfactory'] += 1
        else:
            risk_tier_counts['Good'] += 1

        # Calculate map percentage offsets (calibrated for the relief map of India & subcontinent)
        lat = float(c.latitude)
        lng = float(c.longitude)
        # Lat range ~8 to 34 -> bottom to top (Y: 92% to 15%)
        # Lng range ~68 to 90 -> left to right (X: 18% to 85%)
        y_pct = round(max(10.0, min(88.0, 92.0 - ((lat - 8.0) / (34.5 - 8.0)) * 74.0)), 2)
        x_pct = round(max(12.0, min(86.0, 18.0 + ((lng - 68.0) / (90.0 - 68.0)) * 66.0)), 2)

        point = {
            'id': c.id,
            'name': c.name,
            'state': c.state,
            'slug': c.slug,
            'x': x_pct,
            'y': y_pct,
            'aqi': aqi_val,
            'pm25': aq.pm25 if aq else 35.0,
            'pm10': aq.pm10 if aq else 65.0,
            'temp': wt.temperature if wt else 26.0,
            'condition': wt.condition if wt else 'Clear',
            'dominant': an.dominant_pollutant if an else 'PM2.5',
            'risk_level': risk_lvl,
            'risk_color': aq.get_risk_color() if aq else '#10b981',
            'score': an.environmental_score if an else 75.0,
            'traffic': aq.traffic_level if aq else 'Moderate',
            'recommendation': an.recommendation if an else 'Ambient conditions acceptable.',
            'is_metro': c.is_metro
        }
        city_map_points.append(point)
        top_risk_regions.append(point)

    # Sort top risk regions by highest AQI
    top_risk_regions.sort(key=lambda x: x['aqi'], reverse=True)

    all_latest_aq = [c.latest_air_quality for c in cities if c.latest_air_quality]
    avg_national_aqi = round(sum(a.aqi for a in all_latest_aq) / len(all_latest_aq)) if all_latest_aq else 0
    severe_cities_count = sum(1 for a in all_latest_aq if a.aqi > 200)

    context = {
        'cities': cities,
        'selected_city': selected_city,
        'latest_aq': latest_aq,
        'latest_wt': latest_wt,
        'latest_an': latest_an,
        'aqi_trend': aqi_trend,
        'pm25_trend': pm25_trend,
        'temp_trend': temp_trend,
        'pollutant_percentages': pollutant_percentages,
        'pollutant_percentages_json': json.dumps(pollutant_percentages),
        'trend_data_json': json.dumps(trend_data),
        'avg_national_aqi': avg_national_aqi,
        'severe_cities_count': severe_cities_count,
        'total_cities_count': cities.count(),
        'city_map_points': city_map_points,
        'city_map_points_json': json.dumps(city_map_points),
        'top_risk_regions': top_risk_regions[:5],
        'risk_tier_counts': risk_tier_counts,
    }
    return render(request, 'dashboard/index.html', context)

def compare_view(request):
    cities = City.objects.all().order_by('name')
    city_ids = request.GET.getlist('c')

    # Defaults to Delhi, Mumbai, Bengaluru if none provided
    if not city_ids:
        default_names = ['Delhi', 'Mumbai', 'Bengaluru']
        selected_cities = list(City.objects.filter(name__in=default_names))
    else:
        selected_cities = list(City.objects.filter(id__in=city_ids))

    # Compile data for comparison cards & charts
    comparison_cards = []
    chart_labels = []
    chart_aqi = []
    chart_pm25 = []
    chart_pm10 = []
    chart_temp = []
    chart_humidity = []
    chart_score = []

    for c in selected_cities:
        aq = c.latest_air_quality
        wt = c.latest_weather
        an = c.latest_analysis
        score = aq.calculate_environmental_score() if aq else 0
        risk = aq.get_risk_level() if aq else 'Unknown'
        risk_color = aq.get_risk_color() if aq else '#64748b'

        card = {
            'city': c,
            'aq': aq,
            'wt': wt,
            'an': an,
            'score': score,
            'risk': risk,
            'risk_color': risk_color,
        }
        comparison_cards.append(card)

        chart_labels.append(c.name)
        chart_aqi.append(aq.aqi if aq else 0)
        chart_pm25.append(aq.pm25 if aq else 0)
        chart_pm10.append(aq.pm10 if aq else 0)
        chart_temp.append(wt.temperature if wt else 0)
        chart_humidity.append(wt.humidity if wt else 0)
        chart_score.append(score)

    compare_chart_data = {
        'labels': chart_labels,
        'aqi': chart_aqi,
        'pm25': chart_pm25,
        'pm10': chart_pm10,
        'temp': chart_temp,
        'humidity': chart_humidity,
        'score': chart_score,
    }

    selected_ids = [c.id for c in selected_cities]

    context = {
        'cities': cities,
        'selected_cities': selected_cities,
        'selected_ids': selected_ids,
        'comparison_cards': comparison_cards,
        'compare_chart_data_json': json.dumps(compare_chart_data),
    }
    return render(request, 'dashboard/compare.html', context)

def about_view(request):
    return render(request, 'dashboard/about.html')

def api_city_search(request):
    query = request.GET.get('term', '').strip()
    if not query:
        return JsonResponse([], safe=False)

    cities = City.objects.filter(
        Q(name__icontains=query) | Q(state__icontains=query)
    )[:8]

    results = []
    for c in cities:
        aq = c.latest_air_quality
        results.append({
            'id': c.id,
            'name': c.name,
            'state': c.state,
            'slug': c.slug,
            'aqi': aq.aqi if aq else 'N/A',
            'risk': aq.get_risk_level() if aq else 'N/A',
            'risk_color': aq.get_risk_color() if aq else '#64748b'
        })
    return JsonResponse(results, safe=False)

def api_dashboard_data(request):
    """Clean REST API returning all cities, risk tiers, and latest telemetry for decoupled frontends"""
    cities = City.objects.all().order_by('name')
    city_map_points = []
    
    for c in cities:
        aq = c.latest_air_quality
        wt = c.latest_weather
        an = c.latest_analysis
        lat = float(c.latitude)
        lng = float(c.longitude)
        y_pct = round(max(10.0, min(88.0, 92.0 - ((lat - 8.0) / (34.5 - 8.0)) * 74.0)), 2)
        x_pct = round(max(12.0, min(86.0, 18.0 + ((lng - 68.0) / (90.0 - 68.0)) * 66.0)), 2)

        city_map_points.append({
            'id': c.id,
            'name': c.name,
            'state': c.state,
            'slug': c.slug,
            'x': x_pct,
            'y': y_pct,
            'aqi': aq.aqi if aq else 100,
            'pm25': aq.pm25 if aq else 35.0,
            'pm10': aq.pm10 if aq else 65.0,
            'no2': aq.no2 if aq else 25.0,
            'so2': aq.so2 if aq else 15.0,
            'co': aq.co if aq else 0.8,
            'temp': wt.temperature if wt else 26.0,
            'humidity': wt.humidity if wt else 55.0,
            'condition': wt.condition if wt else 'Clear',
            'dominant': an.dominant_pollutant if an else 'PM2.5',
            'risk_level': an.risk_level if an else 'Moderate',
            'risk_color': aq.get_risk_color() if aq else '#10b981',
            'score': an.environmental_score if an else 75.0,
            'traffic': aq.traffic_level if aq else 'Moderate',
            'recommendation': an.recommendation if an else 'Ambient conditions acceptable.'
        })

    all_latest_aq = [c.latest_air_quality for c in cities if c.latest_air_quality]
    avg_national_aqi = round(sum(a.aqi for a in all_latest_aq) / len(all_latest_aq)) if all_latest_aq else 0

    return JsonResponse({
        'status': 'success',
        'total_cities': len(city_map_points),
        'avg_national_aqi': avg_national_aqi,
        'cities': city_map_points
    })


def api_sync_city(request, slug):
    city = get_object_or_404(City, slug=slug)
    aq, wt = sync_city_realtime_data(city)
    an = city.latest_analysis

    return JsonResponse({
        'status': 'success',
        'city': city.name,
        'slug': city.slug,
        'aqi': aq.aqi if aq else 0,
        'risk_level': aq.get_risk_level() if aq else 'Unknown',
        'risk_color': aq.get_risk_color() if aq else '#10b981',
        'pm25': aq.pm25 if aq else 0,
        'pm10': aq.pm10 if aq else 0,
        'no2': aq.no2 if aq else 0,
        'so2': aq.so2 if aq else 0,
        'co': aq.co if aq else 0,
        'o3': aq.o3 if aq else 0,
        'temp': wt.temperature if wt else 0,
        'humidity': wt.humidity if wt else 0,
        'condition': wt.condition if wt else 'Clear',
        'traffic': aq.traffic_level if aq else 'Moderate',
        'dominant': an.dominant_pollutant if an else 'PM2.5',
        'recommendation': an.recommendation if an else '',
    })

