from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')

    first_name = models.CharField(max_length=150, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=150, blank=True, verbose_name='Фамилия')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        TRANSFER = 'transfer', 'Перевод на счет'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    course = models.ForeignKey(
        'lms.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        'lms.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name='Способ оплаты'
    )
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID сессии Stripe'
    )
    stripe_payment_status = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Статус платежа'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f'Платеж {self.user.email} - {self.amount}'


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        'lms.Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        unique_together = ('user', 'course')  # Уникальность пары user + course
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user.email} подписан на {self.course.name}'
