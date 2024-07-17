from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import (
    CategoryViewSet, CourseViewSet, LessonViewSet, UserCommentsViewSet, 
    LessonVideoViewSet, Filter, SendMassageAPIView, LikeAPIView
)

from rest_framework import routers


router = routers.SimpleRouter()
router.register('category-course', CategoryViewSet)
router.register('course-list', CourseViewSet)
router.register('lessons', LessonViewSet)
router.register('user-comments', UserCommentsViewSet)
router.register('lessons-video', LessonVideoViewSet)


urlpatterns = [
    # Filterlash uchun urls
    path('filter/', Filter.as_view()),
    # Foydalanuvchilarni emailiga yuborish uchun urls
    path('send-massege/', SendMassageAPIView.as_view()),
    # Darsga like bosish uchun urls
    path('like/', LikeAPIView.as_view()),
    # Routerlarga urls
    path('', include(router.urls)),
]