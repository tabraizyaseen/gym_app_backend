from rest_framework import serializers

from .models import User

class ReturningUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=120, required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

class NewUserSerializer(ReturningUserSerializer):

    def validate_email(self, value):
        "validating if email already exists"
        if value and User.objects.filter(email__exact=value).exists():
            raise serializers.ValidationError("this email already exists")
        return value
