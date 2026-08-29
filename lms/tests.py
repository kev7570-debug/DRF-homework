from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Course, Lesson

User = get_user_model()


class LessonTests(APITestCase):

    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123',
            first_name='Test',
            last_name='User'
        )
        # Создаём курс
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        # URL для списка уроков
        self.lessons_url = reverse('lesson-list-create')  # Имя из urls.py

    def test_create_lesson(self):
        """Тест создания урока"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test Lesson',
            'description': 'Test Description',
            'video_url': 'https://www.youtube.com/watch?v=abc123',
            'course': self.course.id
        }
        response = self.client.post(self.lessons_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.first().name, 'Test Lesson')
        self.assertEqual(Lesson.objects.first().owner, self.user)

    def test_create_lesson_invalid_video_url(self):
        """Тест создания урока с невалидной ссылкой"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Test Lesson',
            'description': 'Test Description',
            'video_url': 'https://vk.com/video',
            'course': self.course.id
        }
        response = self.client.post(self.lessons_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_get_lessons_list(self):
        """Тест получения списка уроков"""
        self.client.force_authenticate(user=self.user)
        Lesson.objects.create(
            name='Lesson 1',
            description='Description 1',
            video_url='https://www.youtube.com/watch?v=abc123',
            course=self.course,
            owner=self.user
        )
        response = self.client.get(self.lessons_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Пагинация

    def test_update_lesson(self):
        """Тест обновления урока"""
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(
            name='Old Name',
            description='Old Description',
            video_url='https://www.youtube.com/watch?v=abc123',
            course=self.course,
            owner=self.user
        )
        url = reverse('lesson-detail', args=[lesson.id])
        data = {
            'name': 'New Name',
            'description': 'New Description',
            'video_url': 'https://www.youtube.com/watch?v=xyz789',
            'course': self.course.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lesson.refresh_from_db()
        self.assertEqual(lesson.name, 'New Name')

    def test_delete_lesson(self):
        """Тест удаления урока"""
        self.client.force_authenticate(user=self.user)
        lesson = Lesson.objects.create(
            name='Lesson to Delete',
            description='Description',
            video_url='https://www.youtube.com/watch?v=abc123',
            course=self.course,
            owner=self.user
        )
        url = reverse('lesson-detail', args=[lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

class SubscriptionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test123'
        )
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description'
        )
        self.subscription_url = reverse('subscription')

    def test_add_subscription(self):
        """Тест добавления подписки"""
        self.client.force_authenticate(user=self.user)
        data = {'course': self.course.id}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(self.course.subscriptions.filter(user=self.user).exists())

    def test_remove_subscription(self):
        """Тест удаления подписки"""
        self.client.force_authenticate(user=self.user)
        from users.models import Subscription
        Subscription.objects.create(user=self.user, course=self.course)
        data = {'course': self.course.id}
        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(self.course.subscriptions.filter(user=self.user).exists())
