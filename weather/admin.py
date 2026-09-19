from django.contrib import admin
from .models import Weather

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('city', 'recorded_date', 'temperature', 'humidity', 'wind_speed', 'condition')
    search_fields = ('city__name', 'city__state')
    list_filter = ('condition', 'recorded_date', 'city')
    ordering = ('-recorded_date', 'city')
