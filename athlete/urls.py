from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.registerAthlete.as_view(), name='registration'),
]
