from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Snake


class SnakeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Snake
        fields = ('id', 'owner', 'name', 'description', 'created_at',)

    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username',)