import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from .models import City
from accounts.models import FavoriteCity
from dashboard.services import sync_city_realtime_data

def city_list(request):
    query = request.GET.get('q', '').strip()
    state_filter = request.GET.get('state', '').strip()
    metro_only = request.GET.get('metro', '').strip()
    sort_by = request.GET.get('sort', 'name')

    cities = City.objects.all()

    if query:
        cities = cities.filter(Q(name__icontains=query) | Q(state__icontains=query))
    if state_filter:
        cities = cities.filter(state__iexact=state_filter)
    if metro_only == 'true':
        cities = cities.filter(is_metro=True)

    city_data_list = []
    for c in cities:
        aq = c.latest_air_quality
        wt = c.latest_weather
        an = c.latest_analysis
        city_data_list.append({
            'city': c,
            'aq': aq,
            'weather': wt,
            'analysis': an,
            'aqi': aq.aqi if aq else 0,
            'risk_level': aq.get_risk_level() if aq else 'Unknown',
            'score': aq.calculate_environmental_score() if aq else 0,
            'temp': wt.temperature if wt else 0,
            'risk_color': aq.get_risk_color() if aq else '#64748b',
        })

    if sort_by == 'aqi_desc':
        city_data_list.sort(key=lambda x: x['aqi'], reverse=True)
    elif sort_by == 'aqi_asc':
        city_data_list.sort(key=lambda x: x['aqi'])
    elif sort_by == 'score':
        city_data_list.sort(key=lambda x: x['score'], reverse=True)
    else:
        city_data_list.sort(key=lambda x: x['city'].name)

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = list(FavoriteCity.objects.filter(user=request.user).values_list('city_id', flat=True))

    all_states = City.objects.values_list('state', flat=True).distinct().order_by('state')

    context = {
        'city_data_list': city_data_list,
        'query': query,
        'state_filter': state_filter,
        'metro_only': metro_only,
        'sort_by': sort_by,
        'all_states': all_states,
        'user_favorites': user_favorites,
        'total_cities': len(city_data_list)
    }
    return render(request, 'cities/list.html', context)

def city_detail(request, slug):
    city = get_object_or_404(City, slug=slug)

    # Automatically sync live atmospheric & air telemetry for this city
    try:
        sync_city_realtime_data(city)
    except Exception:
        pass

    latest_aq = city.latest_air_quality
    latest_wt = city.latest_weather
    latest_an = city.latest_analysis

    # 14 days of history for charts
    history_aq = city.air_quality_records.order_by('recorded_date')[:15]
    history_wt = city.weather_records.order_by('recorded_date')[:15]

    dates_labels = [rec.recorded_date.strftime('%d %b') for rec in history_aq]
    aqi_values = [rec.aqi for rec in history_aq]
    pm25_values = [rec.pm25 for rec in history_aq]
    pm10_values = [rec.pm10 for rec in history_aq]
    temp_values = [rec.temperature for rec in history_wt]
    humidity_values = [rec.humidity for rec in history_wt]

    chart_history = {
        'labels': dates_labels,
        'aqi': aqi_values,
        'pm25': pm25_values,
        'pm10': pm10_values,
        'temp': temp_values,
        'humidity': humidity_values,
    }

    percentages = latest_aq.get_pollutant_percentages() if latest_aq else {}

    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = FavoriteCity.objects.filter(user=request.user, city=city).exists()

    context = {
        'city': city,
        'latest_aq': latest_aq,
        'latest_wt': latest_wt,
        'latest_an': latest_an,
        'chart_history_json': json.dumps(chart_history),
        'percentages': percentages,
        'percentages_json': json.dumps(percentages),
        'is_favorited': is_favorited,
        'recent_records': city.air_quality_records.order_by('-recorded_date')[:7]
    }
    return render(request, 'cities/detail.html', context)

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='accounts:login')
def city_add(request):
    """Admin-only view to add an Indian city to the environmental monitoring system."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        state = request.POST.get('state', '').strip()
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()
        population = request.POST.get('population', '').strip() or '1000000'
        description = request.POST.get('description', '').strip()
        is_metro = request.POST.get('is_metro') == 'on'

        if not name or not state or not latitude or not longitude:
            messages.error(request, 'Please provide City Name, State, Latitude, and Longitude.')
            return render(request, 'cities/add.html')

        try:
            lat_f = float(latitude)
            lng_f = float(longitude)
            pop_i = int(population)
        except ValueError:
            messages.error(request, 'Latitude, Longitude, and Population must be valid numbers.')
            return render(request, 'cities/add.html')

        if City.objects.filter(name__iexact=name).exists():
            messages.error(request, f'City "{name}" already exists in the system.')
            return render(request, 'cities/add.html')

        city = City.objects.create(
            name=name,
            slug=slugify(name),
            state=state,
            latitude=lat_f,
            longitude=lng_f,
            population=pop_i,
            description=description or f"Rapidly growing urban center in {state}, actively monitored for air quality and heat index.",
            is_metro=is_metro
        )

        # Trigger initial real-time telemetry sync from Open-Meteo
        try:
            sync_city_realtime_data(city)
            messages.success(request, f'Successfully registered {city.name}! Live satellite & air telemetry synced.')
        except Exception as e:
            messages.success(request, f'Registered {city.name}. Telemetry will update on next automated cycle.')

        return redirect('cities:detail', slug=city.slug)

    return render(request, 'cities/add.html')

@user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='accounts:login')
def city_delete(request, slug):
    """Admin-only view to remove a city from the monitoring system."""
    city = get_object_or_404(City, slug=slug)
    if request.method == 'POST':
        city_name = city.name
        city.delete()
        messages.success(request, f'City "{city_name}" has been permanently removed by admin.')
        return redirect('cities:list')
    return render(request, 'cities/delete_confirm.html', {'city': city})

