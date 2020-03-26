from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, SnakeViewSet


router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('snakes', SnakeViewSet, basename='snakes')

urlpatterns = router.urls