from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Snake
from .permissions import IsOwnerOrReadOnly
from .serializers import SnakeSerializer, UserSerializer


class SnakeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Snake.objects.all()
    serializer_class = SnakeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
