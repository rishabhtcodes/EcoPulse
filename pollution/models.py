from django.db import models
from cities.models import City

class AirQuality(models.Model):
    TRAFFIC_CHOICES = [
        ('Low', 'Low'),
        ('Moderate', 'Moderate'),
        ('Heavy', 'Heavy'),
        ('Severe', 'Severe'),
    ]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='air_quality_records')
    recorded_date = models.DateField()
    aqi = models.IntegerField(help_text='Air Quality Index (0 - 500)')
    pm25 = models.FloatField(help_text='PM2.5 concentration in ug/m3')
    pm10 = models.FloatField(help_text='PM10 concentration in ug/m3')
    co = models.FloatField(help_text='Carbon Monoxide in mg/m3')
    no2 = models.FloatField(help_text='Nitrogen Dioxide in ug/m3')
    so2 = models.FloatField(help_text='Sulphur Dioxide in ug/m3')
    o3 = models.FloatField(help_text='Ozone in ug/m3')
    traffic_level = models.CharField(max_length=20, choices=TRAFFIC_CHOICES, default='Moderate')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Air Quality Record'
        verbose_name_plural = 'Air Quality Records'
        ordering = ['-recorded_date']
        unique_together = ('city', 'recorded_date')

    def __str__(self):
        return f'{self.city.name} - AQI: {self.aqi} on {self.recorded_date}'

    def get_risk_level(self):
        if self.aqi <= 50:
            return 'Good'
        elif self.aqi <= 100:
            return 'Satisfactory'
        elif self.aqi <= 200:
            return 'Moderate'
        elif self.aqi <= 300:
            return 'Poor'
        elif self.aqi <= 400:
            return 'Very Poor'
        else:
            return 'Severe'

    def get_risk_color(self):
        if self.aqi <= 50:
            return '#10b981'
        elif self.aqi <= 100:
            return '#059669'
        elif self.aqi <= 200:
            return '#f59e0b'
        elif self.aqi <= 300:
            return '#f97316'
        elif self.aqi <= 400:
            return '#ef4444'
        else:
            return '#7f1d1d'

    def get_dominant_pollutant(self):
        ratios = {
            'PM2.5': self.pm25 / 60.0,
            'PM10': self.pm10 / 100.0,
            'NO2': self.no2 / 80.0,
            'SO2': self.so2 / 80.0,
            'CO': self.co / 2.0,
            'O3': self.o3 / 100.0,
        }
        return max(ratios.items(), key=lambda x: x[1])[0]

    def get_pollutant_percentages(self):
        raw_vals = {
            'PM2.5': max(0.1, self.pm25),
            'PM10': max(0.1, self.pm10),
            'NO2': max(0.1, self.no2),
            'SO2': max(0.1, self.so2),
            'CO': max(0.1, self.co * 10),
            'O3': max(0.1, self.o3),
        }
        total = sum(raw_vals.values())
        return {k: round((v / total) * 100, 1) for k, v in raw_vals.items()}

    def calculate_environmental_score(self):
        penalty = (self.aqi / 500.0) * 65.0 + min(35.0, (self.pm25 / 250.0) * 35.0)
        return round(max(5.0, min(100.0, 100.0 - penalty)), 1)


class EnvironmentalAnalysis(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='analyses')
    air_quality = models.OneToOneField(AirQuality, on_delete=models.CASCADE, related_name='analysis')
    environmental_score = models.FloatField(help_text='Calculated Score from 0 to 100')
    risk_level = models.CharField(max_length=50)
    dominant_pollutant = models.CharField(max_length=50)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Environmental Analyses'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.city.name} - {self.risk_level}'
