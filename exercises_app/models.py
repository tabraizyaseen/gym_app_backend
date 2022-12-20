from django.db import models

from athlete.models import User

# Create your models here.
class Equipments(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'equipments'
        verbose_name = 'Equipments'
        verbose_name_plural = 'Equipments'

class Excercises(models.Model):
    duration = models.IntegerField()
    description = models.TextField()
    equipment = models.ForeignKey(Equipments, null=True, on_delete=models.SET_NULL)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    calories_burnt = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'excercises'
        verbose_name = 'Excercises'
        verbose_name_plural = 'Excercises'