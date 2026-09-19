from django.urls import path
from . import views

app_name = 'pollution'

urlpatterns = [
    path('', views.analytics_view, name='analytics'),
]
