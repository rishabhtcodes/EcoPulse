from django.contrib import admin
from .models import City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'population', 'is_metro', 'latitude', 'longitude', 'created_at')
    search_fields = ('name', 'state')
    list_filter = ('is_metro', 'state')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
