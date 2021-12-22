from django.urls import path
from .views import VideoQuery, index,VideosView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('api/videolist',VideosView, basename = 'videolist')

urlpatterns = [
   path('',index, name = "index"),
   path('api/search/',VideoQuery.as_view(),name = "videoquery")
] + router.urls
