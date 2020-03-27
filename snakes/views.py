from django.contrib.auth import get_user_model
from rest_framework import viewsets

from .models import Snake
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import SnakeSerializer, UserSerializer


class SnakeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Snake.objects.all()
    serializer_class = SnakeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated, ]
        else:
            self.permission_classes = [IsAdminUser, ]

        return super(UserViewSet, self).get_permissions()