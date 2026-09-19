from django.db import models
from cities.models import City

class Weather(models.Model):
    CONDITION_CHOICES = [
        ('Clear', 'Clear / Sunny'),
        ('Partly Cloudy', 'Partly Cloudy'),
        ('Cloudy', 'Cloudy'),
        ('Hazy', 'Hazy / Smog'),
        ('Rainy', 'Rainy'),
        ('Thunderstorm', 'Thunderstorm'),
    ]

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_records')
    recorded_date = models.DateField()
    temperature = models.FloatField(help_text='Temperature in degrees Celsius')
    humidity = models.FloatField(help_text='Humidity percentage (0 - 100)')
    rainfall = models.FloatField(help_text='Rainfall in mm', default=0.0)
    wind_speed = models.FloatField(help_text='Wind speed in km/h')
    pressure = models.FloatField(help_text='Atmospheric pressure in hPa', default=1013.25)
    condition = models.CharField(max_length=30, choices=CONDITION_CHOICES, default='Clear')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Weather Record'
        verbose_name_plural = 'Weather Records'
        ordering = ['-recorded_date']
        unique_together = ('city', 'recorded_date')

    def __str__(self):
        return f'{self.city.name} - {self.temperature}°C ({self.condition}) on {self.recorded_date}'

    def get_comfort_index(self):
        # 18-26C is comfortable, humidity 30-60%
        temp_comfort = 100 - abs(self.temperature - 24) * 3
        hum_comfort = 100 - abs(self.humidity - 45) * 1.5
        score = max(10, min(100, (temp_comfort * 0.6) + (hum_comfort * 0.4)))
        return round(score, 1)
