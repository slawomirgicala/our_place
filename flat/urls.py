from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='flat-home'),
    path('about/', views.about, name='about-app'),
]
