from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('', views.city_list, name='list'),
    path('<slug:slug>/', views.city_detail, name='detail'),
]
