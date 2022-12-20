from django.urls import path

from . import views

urlpatterns = [
    path('', views.recordExercise.as_view(), name='do_excercise'),
    path('report/', views.exerciseReport.as_view(), name='excercises_report'),
    path('equipment/', views.registerEquipment.as_view(), name='register_equipment'),
]
