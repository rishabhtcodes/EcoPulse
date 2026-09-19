import urllib.request
import json
import logging
from datetime import date
from django.utils import timezone
from cities.models import City
from pollution.models import AirQuality, EnvironmentalAnalysis
from weather.models import Weather

logger = logging.getLogger(__name__)

def sync_city_realtime_data(city):
    """
    Fetches live air quality & weather data for the given city from Open-Meteo
    and updates or creates today's records in the database.
    Free, no API key needed, unlimited calls.
    """
    lat = float(city.latitude)
    lng = float(city.longitude)
    today = timezone.now().date()

    # 1. Fetch live Air Quality
    aq_url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={lat}&longitude={lng}&"
        f"current=european_aqi,us_aqi,pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone"
    )

    aq_data = None
    try:
        req = urllib.request.Request(aq_url, headers={'User-Agent': 'EcoPulse/1.0'})
        with urllib.request.urlopen(req, timeout=6) as res:
            aq_json = json.loads(res.read().decode('utf-8'))
            aq_data = aq_json.get('current')
    except Exception as e:
        logger.warning(f"Failed to fetch live AQ data for {city.name}: {e}")

    # 2. Fetch live Weather
    wt_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lng}&"
        f"current=temperature_2m,relative_humidity_2m,precipitation,surface_pressure,wind_speed_10m,weather_code"
    )

    wt_data = None
    try:
        req = urllib.request.Request(wt_url, headers={'User-Agent': 'EcoPulse/1.0'})
        with urllib.request.urlopen(req, timeout=6) as res:
            wt_json = json.loads(res.read().decode('utf-8'))
            wt_data = wt_json.get('current')
    except Exception as e:
        logger.warning(f"Failed to fetch live weather data for {city.name}: {e}")

    # Update or create AirQuality record
    updated_aq = None
    if aq_data:
        # Us aqi or calculate estimate
        aqi_val = int(aq_data.get('us_aqi') or aq_data.get('european_aqi') or 100)
        pm25_val = float(aq_data.get('pm2_5') or 35.0)
        pm10_val = float(aq_data.get('pm10') or 60.0)
        co_val = round(float(aq_data.get('carbon_monoxide') or 800.0) / 1000.0, 2)  # Convert ug/m3 to mg/m3
        no2_val = float(aq_data.get('nitrogen_dioxide') or 20.0)
        so2_val = float(aq_data.get('sulphur_dioxide') or 12.0)
        o3_val = float(aq_data.get('ozone') or 30.0)

        traffic = 'Heavy' if aqi_val > 250 else ('Moderate' if aqi_val > 100 else 'Low')

        updated_aq, _ = AirQuality.objects.update_or_create(
            city=city,
            recorded_date=today,
            defaults={
                'aqi': aqi_val,
                'pm25': pm25_val,
                'pm10': pm10_val,
                'co': co_val,
                'no2': no2_val,
                'so2': so2_val,
                'o3': o3_val,
                'traffic_level': traffic,
            }
        )

        # Update EnvironmentalAnalysis
        score = updated_aq.calculate_environmental_score()
        risk = updated_aq.get_risk_level()
        dominant = updated_aq.get_dominant_pollutant()

        recommendations = {
            'Good': 'Air quality is excellent. Ideal for outdoor exercise and open ventilation.',
            'Satisfactory': 'Air quality is acceptable. Sensitive individuals should observe standard precautions.',
            'Moderate': 'Moderate particulate presence. Sensitive groups may experience minor respiratory symptoms.',
            'Poor': 'Elevated pollutant levels. Consider limiting prolonged high-intensity outdoor activity.',
            'Very Poor': 'High pollution warning. Active air filtration recommended; wear N95 outdoors.',
            'Severe': 'Emergency pollution alert. Avoid outdoor exposure, seal indoor spaces, and use air purification.'
        }
        rec_text = recommendations.get(risk, 'Follow regional municipal air safety advisories.')

        EnvironmentalAnalysis.objects.update_or_create(
            city=city,
            air_quality=updated_aq,
            defaults={
                'environmental_score': score,
                'risk_level': risk,
                'dominant_pollutant': dominant,
                'recommendation': rec_text,
            }
        )

    # Update or create Weather record
    updated_wt = None
    if wt_data:
        temp = float(wt_data.get('temperature_2m') or 28.0)
        humidity = float(wt_data.get('relative_humidity_2m') or 60.0)
        rainfall = float(wt_data.get('precipitation') or 0.0)
        wind_speed = float(wt_data.get('wind_speed_10m') or 8.0)
        pressure = float(wt_data.get('surface_pressure') or 1010.0)
        weather_code = wt_data.get('weather_code', 0)

        # Map weather codes
        if weather_code in [0, 1]:
            condition = 'Clear'
        elif weather_code in [2]:
            condition = 'Partly Cloudy'
        elif weather_code in [3]:
            condition = 'Cloudy'
        elif weather_code in [45, 48]:
            condition = 'Hazy'
        elif weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            condition = 'Rainy'
        elif weather_code in [95, 96, 99]:
            condition = 'Thunderstorm'
        else:
            condition = 'Clear'

        updated_wt, _ = Weather.objects.update_or_create(
            city=city,
            recorded_date=today,
            defaults={
                'temperature': temp,
                'humidity': humidity,
                'rainfall': rainfall,
                'wind_speed': wind_speed,
                'pressure': pressure,
                'condition': condition,
            }
        )

    return updated_aq, updated_wt
