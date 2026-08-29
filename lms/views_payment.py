from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Course
from .services import create_product, create_price, create_checkout_session
from users.models import Payment


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Создаём продукт в Stripe
        product = create_product(course.name)
        if not product:
            return Response({'error': 'Ошибка создания продукта'}, status=400)

        # Создаём цену в Stripe (сумма в копейках)
        price = create_price(product.id, int(course.price * 100))  # если есть поле price
        if not price:
            return Response({'error': 'Ошибка создания цены'}, status=400)

        # Создаём сессию оплаты
        session = create_checkout_session(price.id)
        if not session:
            return Response({'error': 'Ошибка создания сессии'}, status=400)

        # Сохраняем платёж в базе
        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,  # если есть поле price
            payment_method='transfer',
            stripe_session_id=session.id,
            stripe_payment_status=session.payment_status,
        )

        return Response({
            'payment_id': payment.id,
            'payment_url': session.url,
            'message': 'Ссылка на оплату создана'
        })
