from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Создание и удаление запрещены модераторам
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['list', 'retrieve']:
            # Просмотр доступен всем авторизованным
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            # Обновление: только владелец или модератор
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return super().get_permissions()

class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == 'POST':  # Создание
            return [IsAuthenticated(), ~IsModerator()]
        return [IsAuthenticated()]  # Просмотр списка

class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':  # Удаление
            return [IsAuthenticated(), ~IsModerator()]
        elif self.request.method in ['PUT', 'PATCH']:  # Обновление
            return [IsAuthenticated(), IsModerator() | IsOwner()]
        return [IsAuthenticated()]  # Просмотр одного объекта
