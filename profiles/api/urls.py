from django.urls import include, path
from rest_framework.routers import SimpleRouter
from profiles.api.views import (AvatarUpdateView, ProfileViewSet, 
                                ProfileStatusViewSet)


router = SimpleRouter()
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('status', ProfileStatusViewSet, basename="status")

urlpatterns = router.urls

urlpatterns += [
    path("avatar/", AvatarUpdateView.as_view(), name="avatar-update")
]