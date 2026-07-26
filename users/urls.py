from django.urls import path
from .views import PaymentListView, UserRegistrationView

urlpatterns = [
    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]
