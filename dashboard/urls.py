from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare_view, name='compare'),
    path('about/', views.about_view, name='about'),
    path('api/search/', views.api_city_search, name='api_search'),
]
