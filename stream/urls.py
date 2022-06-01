from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register('video-detail', views.VideoViewset)

urlpatterns = [
    path('', include(router.urls))
]