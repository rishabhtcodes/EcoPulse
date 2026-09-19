from django.contrib import admin
from .models import FavoriteCity, UserProfile

@admin.register(FavoriteCity)
class FavoriteCityAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'created_at')
    search_fields = ('user__username', 'city__name')
    list_filter = ('city',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_city', 'theme_preference', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('theme_preference',)
