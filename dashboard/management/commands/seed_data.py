import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cities.models import City
from pollution.models import AirQuality, EnvironmentalAnalysis
from weather.models import Weather
from accounts.models import UserProfile, FavoriteCity

class Command(BaseCommand):
    help = 'Seeds database with realistic environmental and weather data for major Indian cities'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning EcoPulse India database seeding...'))

        # Clear existing data cleanly
        AirQuality.objects.all().delete()
        Weather.objects.all().delete()
        City.objects.all().delete()

        cities_data = [
            {
                'name': 'Delhi',
                'state': 'Delhi (NCT)',
                'population': 32941000,
                'latitude': 28.613939,
                'longitude': 77.209021,
                'is_metro': True,
                'description': 'National Capital Region facing severe seasonal smog, vehicular emissions, and thermal inversions during winter months.',
                'base_aqi': 240,
                'temp_range': (22, 36),
                'humidity_range': (40, 75),
                'traffic': 'Severe',
                'weather_condition': 'Hazy'
            },
            {
                'name': 'Mumbai',
                'state': 'Maharashtra',
                'population': 20961000,
                'latitude': 19.076090,
                'longitude': 72.877426,
                'is_metro': True,
                'description': 'Coastal financial capital with moderate air dispersal buffered by Arabian Sea breezes, though construction activity remains high.',
                'base_aqi': 125,
                'temp_range': (26, 34),
                'humidity_range': (65, 88),
                'traffic': 'Heavy',
                'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Bengaluru',
                'state': 'Karnataka',
                'population': 13608000,
                'latitude': 12.971598,
                'longitude': 77.594562,
                'is_metro': True,
                'description': 'Silicon Valley of India situated at high altitude, enjoying temperate climate but experiencing rising particulate levels along tech corridors.',
                'base_aqi': 78,
                'temp_range': (19, 29),
                'humidity_range': (45, 70),
                'traffic': 'Heavy',
                'weather_condition': 'Clear'
            },
            {
                'name': 'Chennai',
                'state': 'Tamil Nadu',
                'population': 11503000,
                'latitude': 13.082680,
                'longitude': 80.270718,
                'is_metro': True,
                'description': 'Southern coastal metropolis with significant industrial thermal power zones and maritime humidity balances.',
                'base_aqi': 92,
                'temp_range': (27, 35),
                'humidity_range': (68, 85),
                'traffic': 'Moderate',
                'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Kolkata',
                'state': 'West Bengal',
                'population': 15133000,
                'latitude': 22.572646,
                'longitude': 88.363895,
                'is_metro': True,
                'description': 'Eastern riverine metropolis with high particulate concentrations due to diesel transit, winter low winds, and alluvial dust.',
                'base_aqi': 175,
                'temp_range': (24, 34),
                'humidity_range': (58, 82),
                'traffic': 'Heavy',
                'weather_condition': 'Hazy'
            },
            {
                'name': 'Hyderabad',
                'state': 'Telangana',
                'population': 10534000,
                'latitude': 17.385044,
                'longitude': 78.486671,
                'is_metro': True,
                'description': 'Deccan plateau tech hub balancing dry rocky climate with expanding ring-road industrial and vehicular traffic.',
                'base_aqi': 110,
                'temp_range': (22, 33),
                'humidity_range': (42, 65),
                'traffic': 'Moderate',
                'weather_condition': 'Clear'
            },
            {
                'name': 'Pune',
                'state': 'Maharashtra',
                'population': 6987000,
                'latitude': 18.520430,
                'longitude': 73.856744,
                'is_metro': True,
                'description': 'Automotive and education hub surrounded by Sahyadri foothills, with localized valley pollution pockets.',
                'base_aqi': 95,
                'temp_range': (20, 31),
                'humidity_range': (45, 68),
                'traffic': 'Moderate',
                'weather_condition': 'Clear'
            },
            {
                'name': 'Ahmedabad',
                'state': 'Gujarat',
                'population': 8450000,
                'latitude': 23.022505,
                'longitude': 72.571362,
                'is_metro': True,
                'description': 'Major textile and chemical manufacturing belt with semi-arid conditions causing elevated coarse dust and chemical emissions.',
                'base_aqi': 185,
                'temp_range': (24, 37),
                'humidity_range': (35, 60),
                'traffic': 'Heavy',
                'weather_condition': 'Hazy'
            },
            {
                'name': 'Jaipur',
                'state': 'Rajasthan',
                'population': 4107000,
                'latitude': 26.912434,
                'longitude': 75.787271,
                'is_metro': False,
                'description': 'Pink City surrounded by Aravallis and arid desert fringe, naturally predominated by suspended sand and mineral dust.',
                'base_aqi': 160,
                'temp_range': (23, 36),
                'humidity_range': (30, 52),
                'traffic': 'Moderate',
                'weather_condition': 'Clear'
            },
            {
                'name': 'Chandigarh',
                'state': 'Punjab / Haryana',
                'population': 1215000,
                'latitude': 30.733315,
                'longitude': 76.779418,
                'is_metro': False,
                'description': 'Planned green city with high per-capita vehicle density, subject to agricultural seasonal stubble drift.',
                'base_aqi': 130,
                'temp_range': (18, 32),
                'humidity_range': (40, 65),
                'traffic': 'Moderate',
                'weather_condition': 'Clear'
            },
            {
                'name': 'Lucknow',
                'state': 'Uttar Pradesh',
                'population': 3780000,
                'latitude': 26.846709,
                'longitude': 80.946159,
                'is_metro': False,
                'description': 'Gangetic plain capital suffering from trapped thermal inversion, high biomass usage, and slow wind currents.',
                'base_aqi': 210,
                'temp_range': (21, 35),
                'humidity_range': (48, 78),
                'traffic': 'Heavy',
                'weather_condition': 'Hazy'
            },
            {
                'name': 'Shimla',
                'state': 'Himachal Pradesh',
                'population': 230000,
                'latitude': 31.104829,
                'longitude': 77.173424,
                'is_metro': False,
                'description': 'Himalayan mountain station with pristine coniferous forest air, occasionally spiked only during peak tourist vehicle flow.',
                'base_aqi': 42,
                'temp_range': (8, 20),
                'humidity_range': (50, 75),
                'traffic': 'Low',
                'weather_condition': 'Clear'
            }
        ]

        today = date.today()
        # Create 14 days of historical timeline for each city
        days_history = 14

        total_air_records = 0
        total_weather_records = 0

        for c_dict in cities_data:
            city = City.objects.create(
                name=c_dict['name'],
                state=c_dict['state'],
                population=c_dict['population'],
                latitude=c_dict['latitude'],
                longitude=c_dict['longitude'],
                description=c_dict['description'],
                is_metro=c_dict['is_metro']
            )

            base_aqi = c_dict['base_aqi']
            t_min, t_max = c_dict['temp_range']
            h_min, h_max = c_dict['humidity_range']

            for d_idx in range(days_history, -1, -1):
                rec_date = today - timedelta(days=d_idx)
                
                # Daily variation
                daily_jitter = random.uniform(-0.25, 0.25)
                cur_aqi = int(max(25, min(480, base_aqi * (1 + daily_jitter))))
                
                # Derived realistic pollutant values
                pm25 = round(cur_aqi * random.uniform(0.35, 0.55), 1)
                pm10 = round(pm25 * random.uniform(1.6, 2.3), 1)
                no2 = round(max(10.0, cur_aqi * random.uniform(0.18, 0.32)), 1)
                so2 = round(max(5.0, cur_aqi * random.uniform(0.06, 0.14)), 1)
                co = round(max(0.3, cur_aqi * 0.008 * random.uniform(0.8, 1.3)), 2)
                o3 = round(max(15.0, min(140.0, 30 + random.uniform(5, 55))), 1)

                traffic = c_dict['traffic']
                if d_idx % 7 in [0, 6]:
                    traffic = 'Moderate' if traffic == 'Heavy' else traffic

                air_rec = AirQuality.objects.create(
                    city=city,
                    recorded_date=rec_date,
                    aqi=cur_aqi,
                    pm25=pm25,
                    pm10=pm10,
                    co=co,
                    no2=no2,
                    so2=so2,
                    o3=o3,
                    traffic_level=traffic
                )
                total_air_records += 1

                # Weather record
                temperature = round(random.uniform(t_min, t_max), 1)
                humidity = round(random.uniform(h_min, h_max), 1)
                rainfall = round(random.uniform(0, 15) if random.random() < 0.15 else 0.0, 1)
                wind_speed = round(random.uniform(5.0, 22.0), 1)
                pressure = round(random.uniform(1008.0, 1016.0), 1)
                cond = c_dict['weather_condition']
                if rainfall > 2.0:
                    cond = 'Rainy'
                elif cur_aqi > 250:
                    cond = 'Hazy'

                Weather.objects.create(
                    city=city,
                    recorded_date=rec_date,
                    temperature=temperature,
                    humidity=humidity,
                    rainfall=rainfall,
                    wind_speed=wind_speed,
                    pressure=pressure,
                    condition=cond
                )
                total_weather_records += 1

                # Generate EnvironmentalAnalysis for the record
                risk = air_rec.get_risk_level()
                dominant = air_rec.get_dominant_pollutant()
                env_score = air_rec.calculate_environmental_score()

                if risk in ['Severe', 'Very Poor']:
                    rec = 'Severely elevated particulate pollution. Limit all prolonged outdoor physical exertion. Sensitive groups and children must wear N95 respirators. Keep air purifiers operational.'
                elif risk == 'Poor':
                    rec = 'Unhealthy air index for sensitive groups. Reduce strenuous outdoor morning runs. Ventilate indoor spaces only during afternoon hours with better solar dispersion.'
                elif risk == 'Moderate':
                    rec = 'Moderate ambient air quality. Generally acceptable for public outdoor activity, though sensitive asthmatic individuals should exercise caution.'
                elif risk == 'Satisfactory':
                    rec = 'Satisfactory ambient atmosphere with minimal respiratory hazards. Ideal conditions for outdoor sports, commuting, and green recreation.'
                else:
                    rec = 'Excellent, pristine air quality. Optimal environmental conditions across all health brackets with zero protective precautions required.'

                EnvironmentalAnalysis.objects.create(
                    city=city,
                    air_quality=air_rec,
                    environmental_score=env_score,
                    risk_level=risk,
                    dominant_pollutant=dominant,
                    recommendation=rec
                )

        # Create demo superuser and test user
        if not User.objects.filter(username='admin').exists():
            u = User.objects.create_superuser('admin', 'admin@ecopulse.in', 'admin123')
            UserProfile.objects.create(user=u, theme_preference='dark')
            self.stdout.write(self.style.SUCCESS('Admin user created (user: admin, pass: admin123)'))

        if not User.objects.filter(username='student').exists():
            s = User.objects.create_user('student', 'student@ecopulse.in', 'student123')
            delhi = City.objects.filter(name='Delhi').first()
            UserProfile.objects.create(user=s, default_city=delhi, theme_preference='dark')
            if delhi:
                FavoriteCity.objects.create(user=s, city=delhi)
                mum = City.objects.filter(name='Mumbai').first()
                if mum:
                    FavoriteCity.objects.create(user=s, city=mum)
            self.stdout.write(self.style.SUCCESS('Demo student user created (user: student, pass: student123)'))

        self.stdout.write(self.style.SUCCESS(
            f'Seeding Complete! Successfully created {City.objects.count()} cities, '
            f'{total_air_records} air quality records, and {total_weather_records} weather records.'
        ))
