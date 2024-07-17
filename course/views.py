from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import (
    CategorySerializer, CourseSerializer, UserCommentsSerializer,
    LessonSerializer, LessonVideoSerializer, LikeSerializer, SendMassageSerializer,
)
from .models import (
    Category, Course, UserComments, Lesson, LessonVideo, Like, SendMassage
)

from .permissions import CustomPermission 
from rest_framework import filters


class CategoryViewSet(ModelViewSet):
    """Bu viewset orqali Kurslarni kategoriyasini CRUD qilishimiz mumkin"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name',]
    permission_classes = [CustomPermission]




class CourseViewSet(ModelViewSet):
    """Bu viewset orqali Kurslarni CRUD qilishimiz mumkin"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price']
    permission_classes = [CustomPermission]


class LessonViewSet(ModelViewSet):
    """Bu viewset orqali Darslarni CRUD qilishimiz mumkin"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [CustomPermission]


class UserCommentsViewSet(ModelViewSet):
    """comentariya yozish uchun va data basega saqlash mumkin"""
    queryset = UserComments.objects.all()
    serializer_class = UserCommentsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonVideoViewSet(ModelViewSet):
    """Darslarga video yuklash uchun"""
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [CustomPermission]


class Filter(APIView):
    """Bu view orqali Darslarni nomiga qarab filtrlash mumkin"""
    permission_classes = [permissions.AllowAny]

    def get(self, request: Request):
        word = str(request.query_params.get('word'))
        lesson = Lesson.objects.filter(name__icontains=word)
        return Response({'lesson': LessonSerializer(lesson, many=True).data})


class LikeAPIView(APIView):
    """ Darslarga like/dislike qo'shish uchun"""

    def get(self, request):
        serializer = LikeSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            value = serializer.validated_data.get('like')
            lesson_id = serializer.validated_data.get('lesson')
            lesson = Lesson.objects.get(pk=lesson_id)

            try:
                like = Like.objects.get(
                    lesson=lesson,
                    user=request.user
                )
                like.delete()

            except Like.DoesNotExist:
                Like.objects.create(
                    lesson=lesson,
                    user=request.user,
                    like_or_dislike=value
                )

            return Response({'success': "Muvoffaqiyatli"})


class SendMassageAPIView(APIView):
    """elektron pochtaga habar yuborish"""
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = SendMassage.objects.all()

    def get(self, request: Request):
        serializer = SendMassageSerializer()
        return Response(serializer.data)

    def post(self, request: Request):
        serializer = SendMassageSerializer(data=request.data)
        if serializer.is_valid():
            users = User.objects.all()
            for user in users:
                subject = serializer.validated_data.get('name')
                message = f"Salom {user.username}, {serializer.validated_data.get('message')}"
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)

            send_message = SendMassage(
                name=serializer.validated_data['name'],
                message=serializer.validated_data['message']
            )
            send_message.save()

            return Response({'success': "Xabar Foydalanuvchilarga yuborildi"})
        
        