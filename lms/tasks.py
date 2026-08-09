from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()


@shared_task
def send_course_update_email(course_id):
    """
    Отправляет email всем подписчикам курса об обновлении.
    """
    try:
        course = Course.objects.get(id=course_id)
        subscribers = course.subscriptions.all()

        if not subscribers:
            return f'Нет подписчиков у курса {course.name}'

        for subscription in subscribers:
            user = subscription.user
            send_mail(
                subject=f'Обновление курса: {course.name}',
                message=f'Курс "{course.name}" был обновлён. Проверьте новые материалы!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

        return f'Уведомления отправлены {subscribers.count()} подписчикам курса {course.name}'

    except Course.DoesNotExist:
        return f'Курс с id {course_id} не найден'


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более месяца.
    """
    month_ago = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = users.update(is_active=False)
    return f'Заблокировано {count} неактивных пользователей'
