from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('compare/', views.compare_view, name='compare'),
    path('about/', views.about_view, name='about'),
    path('api/search/', views.api_city_search, name='api_search'),
    path('api/dashboard-data/', views.api_dashboard_data, name='api_dashboard_data'),
    path('api/sync-city/<slug:slug>/', views.api_sync_city, name='api_sync_city'),
]
