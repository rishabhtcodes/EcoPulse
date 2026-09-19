from django.db import models
from django.contrib.auth.models import User
from cities.models import City

class FavoriteCity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'city')
        verbose_name_plural = 'Favorite Cities'

    def __str__(self):
        return f'{self.user.username} - {self.city.name}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    default_city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    theme_preference = models.CharField(max_length=10, default='dark', choices=[('dark', 'Dark'), ('light', 'Light')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
