from rest_framework import serializers

from .models import Equipments, Excercises, User

class EquipmentsSerializer(serializers.ModelSerializer):
    " Registering new equipments serializer "
    name = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = Equipments
        fields = '__all__'

class ExcercisesSerializer(serializers.ModelSerializer):
    " Recording user excercises serializer "
    equipment = serializers.PrimaryKeyRelatedField(queryset=Equipments.objects.all(), required=False)
    athlete = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Excercises
        fields = '__all__'

class ReportSerializer(serializers.Serializer):
    " Generating excercises report serializer "
    start = serializers.DateTimeField(required=True)
    end = serializers.DateTimeField(required=True)
