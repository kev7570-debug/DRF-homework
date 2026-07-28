from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentListView, UserRegistrationView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
