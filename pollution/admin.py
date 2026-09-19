from django.contrib import admin
from .models import AirQuality, EnvironmentalAnalysis

@admin.register(AirQuality)
class AirQualityAdmin(admin.ModelAdmin):
    list_display = ('city', 'recorded_date', 'aqi', 'pm25', 'pm10', 'traffic_level', 'get_risk_level')
    search_fields = ('city__name', 'city__state')
    list_filter = ('traffic_level', 'recorded_date', 'city')
    ordering = ('-recorded_date', 'city')

@admin.register(EnvironmentalAnalysis)
class EnvironmentalAnalysisAdmin(admin.ModelAdmin):
    list_display = ('city', 'risk_level', 'dominant_pollutant', 'environmental_score', 'created_at')
    search_fields = ('city__name', 'dominant_pollutant', 'risk_level')
    list_filter = ('risk_level', 'dominant_pollutant', 'city')
    ordering = ('-created_at',)
