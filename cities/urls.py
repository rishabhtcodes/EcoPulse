from django.urls import path
from . import views

app_name = 'cities'

urlpatterns = [
    path('', views.city_list, name='list'),
    path('add/', views.city_add, name='add'),
    path('<slug:slug>/', views.city_detail, name='detail'),
    path('<slug:slug>/delete/', views.city_delete, name='delete'),
]
