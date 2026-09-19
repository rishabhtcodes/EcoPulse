import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from cities.models import City
from pollution.models import AirQuality, EnvironmentalAnalysis
from weather.models import Weather
from accounts.models import UserProfile, FavoriteCity

class Command(BaseCommand):
    help = 'Seeds database with realistic environmental and weather data for cities across ALL states and union territories of India'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Beginning Pan-India EcoPulse database seeding across all Indian states & UTs...'))

        # Clear existing data cleanly
        AirQuality.objects.all().delete()
        Weather.objects.all().delete()
        City.objects.all().delete()

        # Comprehensive Pan-India dataset covering all 28 States & major UTs
        pan_india_cities = [
            # Northern India
            {
                'name': 'Delhi', 'state': 'Delhi (NCT)', 'population': 32941000,
                'latitude': 28.613939, 'longitude': 77.209021, 'is_metro': True,
                'description': 'National Capital Region facing severe seasonal smog, vehicular emissions, and thermal inversions during winter months.',
                'base_aqi': 240, 'temp_range': (22, 36), 'humidity_range': (40, 75), 'traffic': 'Severe', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Chandigarh', 'state': 'Punjab / Haryana', 'population': 1215000,
                'latitude': 30.733315, 'longitude': 76.779418, 'is_metro': False,
                'description': 'Planned modern union territory with high green tree cover balanced against seasonal stubble haze.',
                'base_aqi': 128, 'temp_range': (18, 32), 'humidity_range': (40, 65), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Lucknow', 'state': 'Uttar Pradesh', 'population': 3780000,
                'latitude': 26.846709, 'longitude': 80.946159, 'is_metro': False,
                'description': 'Gangetic plain hub suffering from slow wind currents, high particulate concentrations, and urban congestion.',
                'base_aqi': 210, 'temp_range': (21, 35), 'humidity_range': (48, 78), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Varanasi', 'state': 'Uttar Pradesh', 'population': 1435000,
                'latitude': 25.317645, 'longitude': 82.973915, 'is_metro': False,
                'description': 'Ancient cultural epicenter along the sacred Ganga with high particulate matter from dense urban corridors and biomass.',
                'base_aqi': 178, 'temp_range': (23, 36), 'humidity_range': (50, 80), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Kanpur', 'state': 'Uttar Pradesh', 'population': 3200000,
                'latitude': 26.449923, 'longitude': 80.331871, 'is_metro': False,
                'description': 'Prominent industrial and leather tanning metropolis experiencing heavy particulate burdens.',
                'base_aqi': 225, 'temp_range': (22, 36), 'humidity_range': (45, 75), 'traffic': 'Severe', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Amritsar', 'state': 'Punjab', 'population': 1300000,
                'latitude': 31.633980, 'longitude': 74.872261, 'is_metro': False,
                'description': 'Major commercial and cultural hub in northwest Punjab subject to regional agricultural dust and transport emissions.',
                'base_aqi': 148, 'temp_range': (19, 34), 'humidity_range': (42, 68), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Ludhiana', 'state': 'Punjab', 'population': 1700000,
                'latitude': 30.900965, 'longitude': 75.857277, 'is_metro': False,
                'description': 'Industrial manufacturing powerhouse with active textile, bicycle, and metal casting emission sources.',
                'base_aqi': 192, 'temp_range': (20, 35), 'humidity_range': (40, 70), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Srinagar', 'state': 'Jammu & Kashmir', 'population': 1273000,
                'latitude': 34.083656, 'longitude': 74.797371, 'is_metro': False,
                'description': 'Kashmir valley capital nestled beside Dal Lake, facing trapped biomass smoke during freezing winter heating cycles.',
                'base_aqi': 68, 'temp_range': (6, 22), 'humidity_range': (55, 82), 'traffic': 'Low', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Jammu', 'state': 'Jammu & Kashmir', 'population': 650000,
                'latitude': 32.726601, 'longitude': 74.857025, 'is_metro': False,
                'description': 'Foothills winter hub characterized by expanding highway logistics, moderate dust, and subtropical valley heat.',
                'base_aqi': 98, 'temp_range': (18, 33), 'humidity_range': (45, 72), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Shimla', 'state': 'Himachal Pradesh', 'population': 230000,
                'latitude': 31.104829, 'longitude': 77.173424, 'is_metro': False,
                'description': 'Himalayan mountain station with pristine coniferous forest air, occasionally elevated during peak tourist vehicle flow.',
                'base_aqi': 42, 'temp_range': (8, 20), 'humidity_range': (50, 75), 'traffic': 'Low', 'weather_condition': 'Clear'
            },
            {
                'name': 'Dehradun', 'state': 'Uttarakhand', 'population': 800000,
                'latitude': 30.316496, 'longitude': 78.032188, 'is_metro': False,
                'description': 'Doan valley capital experiencing expanding urban footprint between Song and Asan river channels.',
                'base_aqi': 94, 'temp_range': (16, 30), 'humidity_range': (52, 78), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },

            # Western India
            {
                'name': 'Mumbai', 'state': 'Maharashtra', 'population': 20961000,
                'latitude': 19.076090, 'longitude': 72.877426, 'is_metro': True,
                'description': 'Coastal financial capital with moderate air dispersal buffered by Arabian Sea breezes, though construction activity remains high.',
                'base_aqi': 115, 'temp_range': (26, 34), 'humidity_range': (65, 88), 'traffic': 'Heavy', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Pune', 'state': 'Maharashtra', 'population': 6987000,
                'latitude': 18.520430, 'longitude': 73.856744, 'is_metro': True,
                'description': 'Automotive and education hub surrounded by Sahyadri foothills, with localized valley pollution pockets.',
                'base_aqi': 88, 'temp_range': (20, 31), 'humidity_range': (45, 68), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Nagpur', 'state': 'Maharashtra', 'population': 2900000,
                'latitude': 21.145800, 'longitude': 79.088158, 'is_metro': False,
                'description': 'Geographic center of India with continental dry heat, transport junctions, and coal-fired thermal generation.',
                'base_aqi': 122, 'temp_range': (22, 37), 'humidity_range': (35, 62), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Ahmedabad', 'state': 'Gujarat', 'population': 8450000,
                'latitude': 23.022505, 'longitude': 72.571362, 'is_metro': True,
                'description': 'Major textile and chemical manufacturing belt with semi-arid conditions causing elevated coarse dust.',
                'base_aqi': 165, 'temp_range': (24, 37), 'humidity_range': (35, 60), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Surat', 'state': 'Gujarat', 'population': 6500000,
                'latitude': 21.170240, 'longitude': 72.831062, 'is_metro': False,
                'description': 'Global diamond and silk textile metropolis with high industrial marine proximity along the Tapi River.',
                'base_aqi': 124, 'temp_range': (25, 35), 'humidity_range': (58, 80), 'traffic': 'Moderate', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Jaipur', 'state': 'Rajasthan', 'population': 4107000,
                'latitude': 26.912434, 'longitude': 75.787271, 'is_metro': False,
                'description': 'Pink City surrounded by Aravallis and arid desert fringe, naturally predominated by suspended sand and mineral dust.',
                'base_aqi': 152, 'temp_range': (23, 36), 'humidity_range': (30, 52), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Jodhpur', 'state': 'Rajasthan', 'population': 1400000,
                'latitude': 26.238947, 'longitude': 73.024307, 'is_metro': False,
                'description': 'Sun City on the edge of the Thar Desert subject to significant wind-blown particulate and dry heat.',
                'base_aqi': 168, 'temp_range': (24, 39), 'humidity_range': (25, 48), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Panaji', 'state': 'Goa', 'population': 120000,
                'latitude': 15.490930, 'longitude': 73.827850, 'is_metro': False,
                'description': 'Mandovi estuary capital enjoying unpolluted oceanic clean air currents, lush tropical forests, and coastal breezes.',
                'base_aqi': 38, 'temp_range': (25, 33), 'humidity_range': (70, 90), 'traffic': 'Low', 'weather_condition': 'Clear'
            },

            # Southern India
            {
                'name': 'Bengaluru', 'state': 'Karnataka', 'population': 13608000,
                'latitude': 12.971598, 'longitude': 77.594562, 'is_metro': True,
                'description': 'Silicon Valley of India situated at high altitude, enjoying temperate climate but experiencing rising particulate levels along tech corridors.',
                'base_aqi': 76, 'temp_range': (19, 29), 'humidity_range': (45, 70), 'traffic': 'Heavy', 'weather_condition': 'Clear'
            },
            {
                'name': 'Chennai', 'state': 'Tamil Nadu', 'population': 11503000,
                'latitude': 13.082680, 'longitude': 80.270718, 'is_metro': True,
                'description': 'Southern coastal metropolis with significant industrial thermal power zones and maritime humidity balances.',
                'base_aqi': 84, 'temp_range': (27, 35), 'humidity_range': (68, 85), 'traffic': 'Moderate', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Coimbatore', 'state': 'Tamil Nadu', 'population': 2800000,
                'latitude': 11.016844, 'longitude': 76.955833, 'is_metro': False,
                'description': 'Manchester of South India situated near Palghat Gap, maintaining clean Western Ghats breezes.',
                'base_aqi': 62, 'temp_range': (22, 32), 'humidity_range': (55, 78), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Hyderabad', 'state': 'Telangana', 'population': 10534000,
                'latitude': 17.385044, 'longitude': 78.486671, 'is_metro': True,
                'description': 'Deccan plateau tech hub balancing dry rocky climate with expanding ring-road industrial and vehicular traffic.',
                'base_aqi': 102, 'temp_range': (22, 33), 'humidity_range': (42, 65), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Visakhapatnam', 'state': 'Andhra Pradesh', 'population': 2300000,
                'latitude': 17.686816, 'longitude': 83.218483, 'is_metro': False,
                'description': 'Coastal port city with major steel and petrochemical refineries buffered by Bay of Bengal winds.',
                'base_aqi': 86, 'temp_range': (26, 34), 'humidity_range': (68, 86), 'traffic': 'Moderate', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Vijayawada', 'state': 'Andhra Pradesh', 'population': 1800000,
                'latitude': 16.506174, 'longitude': 80.648018, 'is_metro': False,
                'description': 'Krishna River delta commercial nexus experiencing heavy freight traffic and warm alluvial conditions.',
                'base_aqi': 95, 'temp_range': (25, 37), 'humidity_range': (58, 82), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Thiruvananthapuram', 'state': 'Kerala', 'population': 1100000,
                'latitude': 8.524139, 'longitude': 76.936638, 'is_metro': False,
                'description': 'Southern coastal capital enjoying exceptionally low industrial particulate loads and continuous sea air flushing.',
                'base_aqi': 35, 'temp_range': (24, 32), 'humidity_range': (72, 90), 'traffic': 'Low', 'weather_condition': 'Clear'
            },
            {
                'name': 'Kochi', 'state': 'Kerala', 'population': 2100000,
                'latitude': 9.931233, 'longitude': 76.267303, 'is_metro': False,
                'description': 'Vibrant port and refinery city with maritime moisture and low baseline atmospheric pollution.',
                'base_aqi': 48, 'temp_range': (25, 33), 'humidity_range': (72, 88), 'traffic': 'Moderate', 'weather_condition': 'Partly Cloudy'
            },

            # Eastern & Central India
            {
                'name': 'Kolkata', 'state': 'West Bengal', 'population': 15133000,
                'latitude': 22.572646, 'longitude': 88.363895, 'is_metro': True,
                'description': 'Eastern riverine metropolis with high particulate concentrations due to diesel transit, winter low winds, and alluvial dust.',
                'base_aqi': 168, 'temp_range': (24, 34), 'humidity_range': (58, 82), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Bhubaneswar', 'state': 'Odisha', 'population': 1200000,
                'latitude': 20.296059, 'longitude': 85.824540, 'is_metro': False,
                'description': 'Temple city with planned sectors, moderate industrial growth, and maritime Bay of Bengal atmospheric influence.',
                'base_aqi': 82, 'temp_range': (24, 35), 'humidity_range': (62, 85), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Patna', 'state': 'Bihar', 'population': 2500000,
                'latitude': 25.594095, 'longitude': 85.137566, 'is_metro': False,
                'description': 'High-density Gangetic plain metropolis prone to seasonal temperature inversion, road dust, and biomass emissions.',
                'base_aqi': 215, 'temp_range': (22, 35), 'humidity_range': (52, 78), 'traffic': 'Severe', 'weather_condition': 'Hazy'
            },
            {
                'name': 'Ranchi', 'state': 'Jharkhand', 'population': 1450000,
                'latitude': 23.344100, 'longitude': 85.309562, 'is_metro': False,
                'description': 'Chota Nagpur plateau capital with pleasant elevation, surrounded by mineral-rich industrial belts.',
                'base_aqi': 118, 'temp_range': (18, 30), 'humidity_range': (48, 72), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Bhopal', 'state': 'Madhya Pradesh', 'population': 2400000,
                'latitude': 23.259933, 'longitude': 77.412615, 'is_metro': False,
                'description': 'City of Lakes in central India with expansive water bodies providing natural thermal and particulate buffering.',
                'base_aqi': 112, 'temp_range': (20, 34), 'humidity_range': (40, 68), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Indore', 'state': 'Madhya Pradesh', 'population': 3200000,
                'latitude': 22.719569, 'longitude': 75.857726, 'is_metro': False,
                'description': 'Cleanest city in India by municipal hygiene, continuously mitigating road dust via systematic street washing.',
                'base_aqi': 96, 'temp_range': (21, 33), 'humidity_range': (38, 65), 'traffic': 'Moderate', 'weather_condition': 'Clear'
            },
            {
                'name': 'Raipur', 'state': 'Chhattisgarh', 'population': 1500000,
                'latitude': 21.251384, 'longitude': 81.629641, 'is_metro': False,
                'description': 'Mineral processing and sponge iron capital with elevated industrial particulate concentrations.',
                'base_aqi': 162, 'temp_range': (23, 37), 'humidity_range': (45, 74), 'traffic': 'Heavy', 'weather_condition': 'Hazy'
            },

            # North-Eastern India
            {
                'name': 'Guwahati', 'state': 'Assam', 'population': 1150000,
                'latitude': 26.144517, 'longitude': 91.736237, 'is_metro': False,
                'description': 'Gateway to Northeast India situated along the Brahmaputra valley with rising urban construction and valley trapping.',
                'base_aqi': 105, 'temp_range': (20, 32), 'humidity_range': (65, 88), 'traffic': 'Moderate', 'weather_condition': 'Partly Cloudy'
            },
            {
                'name': 'Shillong', 'state': 'Meghalaya', 'population': 180000,
                'latitude': 25.578773, 'longitude': 91.893254, 'is_metro': False,
                'description': 'Scotland of the East with lush pine valleys, abundant rainfall, and consistently pure mountain air.',
                'base_aqi': 32, 'temp_range': (11, 23), 'humidity_range': (68, 92), 'traffic': 'Low', 'weather_condition': 'Clear'
            },
            {
                'name': 'Imphal', 'state': 'Manipur', 'population': 280000,
                'latitude': 24.817011, 'longitude': 93.936844, 'is_metro': False,
                'description': 'Scenic valley capital flanked by mountain ridges with negligible heavy industrial pollution.',
                'base_aqi': 44, 'temp_range': (14, 26), 'humidity_range': (62, 85), 'traffic': 'Low', 'weather_condition': 'Clear'
            },
            {
                'name': 'Aizawl', 'state': 'Mizoram', 'population': 310000,
                'latitude': 23.727107, 'longitude': 92.717639, 'is_metro': False,
                'description': 'Mountain ridge city boasting one of the cleanest air quality records in the country.',
                'base_aqi': 28, 'temp_range': (13, 25), 'humidity_range': (65, 88), 'traffic': 'Low', 'weather_condition': 'Clear'
            },
            {
                'name': 'Agartala', 'state': 'Tripura', 'population': 520000,
                'latitude': 23.831457, 'longitude': 91.286778, 'is_metro': False,
                'description': 'Lowland riverine capital with abundant greenery and clean atmospheric conditions.',
                'base_aqi': 64, 'temp_range': (21, 33), 'humidity_range': (65, 86), 'traffic': 'Low', 'weather_condition': 'Clear'
            }
        ]

        today = date.today()
        days_history = 14

        total_air_records = 0
        total_weather_records = 0

        for c_dict in pan_india_cities:
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
                daily_jitter = random.uniform(-0.25, 0.25)
                cur_aqi = int(max(25, min(480, base_aqi * (1 + daily_jitter))))

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
                wind_speed = round(random.uniform(4.0, 24.0), 1)
                pressure = round(random.uniform(1005.0, 1018.0), 1)

                Weather.objects.create(
                    city=city,
                    recorded_date=rec_date,
                    temperature=temperature,
                    humidity=humidity,
                    rainfall=rainfall,
                    wind_speed=wind_speed,
                    pressure=pressure,
                    condition=c_dict['weather_condition']
                )
                total_weather_records += 1

                # Environmental Analysis on the latest record
                if d_idx == 0:
                    score = air_rec.calculate_environmental_score()
                    risk = air_rec.get_risk_level()
                    dominant = air_rec.get_dominant_pollutant()

                    recommendations = {
                        'Good': 'Air quality is pristine. Perfect for all outdoor recreation and unassisted ventilation.',
                        'Satisfactory': 'Air quality is acceptable. Minor particulate sensitivity possible for vulnerable groups.',
                        'Moderate': 'Particulate matter presents moderate risk. Consider reducing prolonged outdoor workouts.',
                        'Poor': 'Noticeable atmospheric stress. Sensitive individuals should wear protective masks.',
                        'Very Poor': 'Significant health hazard. High-efficiency HEPA air filtration recommended indoors.',
                        'Severe': 'Emergency pollution condition. Avoid all outdoor activity; seal windows and run purifiers.'
                    }
                    rec_text = recommendations.get(risk, 'Adhere to local municipal pollution warnings.')

                    EnvironmentalAnalysis.objects.create(
                        city=city,
                        air_quality=air_rec,
                        environmental_score=score,
                        risk_level=risk,
                        dominant_pollutant=dominant,
                        recommendation=rec_text
                    )

        # Ensure demo and admin accounts exist
        admin_user, created_admin = User.objects.get_or_create(username='admin', defaults={'email': 'admin@ecopulse.in', 'is_staff': True, 'is_superuser': True})
        if created_admin:
            admin_user.set_password('admin123')
            admin_user.save()

        student_user, created_student = User.objects.get_or_create(username='student', defaults={'email': 'student@ecopulse.in'})
        if created_student:
            student_user.set_password('student123')
            student_user.save()

        # Seed favorite cities
        delhi_city = City.objects.filter(name='Delhi').first()
        bengaluru_city = City.objects.filter(name='Bengaluru').first()
        mumbai_city = City.objects.filter(name='Mumbai').first()

        UserProfile.objects.get_or_create(user=admin_user, defaults={'default_city': delhi_city})
        profile_student, _ = UserProfile.objects.get_or_create(user=student_user, defaults={'default_city': bengaluru_city})

        if delhi_city:
            FavoriteCity.objects.get_or_create(user=student_user, city=delhi_city)
        if bengaluru_city:
            FavoriteCity.objects.get_or_create(user=student_user, city=bengaluru_city)
        if mumbai_city:
            FavoriteCity.objects.get_or_create(user=student_user, city=mumbai_city)

        self.stdout.write(self.style.SUCCESS(f'Successfully populated database for {len(pan_india_cities)} cities across India!'))
        self.stdout.write(self.style.SUCCESS(f'Created {total_air_records} air quality records and {total_weather_records} weather logs.'))
