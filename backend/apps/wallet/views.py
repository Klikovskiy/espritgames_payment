from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WalletSerializer, TransactionSerializer


class WalletBalanceView(APIView):
    """
    API endpoint для проверки баланса кошелька пользователя.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Успешный запрос баланса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER, example=100.00),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный запрос",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Учетные данные не были предоставлены."),
                    }
                )
            ),
        }
    )
    def get(self, request: Request) -> Response:
        """
        Получить баланс пользователя.

        Параметры запроса:
        - request (Request): Объект запроса.

        Возвращает:
        - Response: JSON-ответ с балансом пользователя.
        """
        wallet = request.user.wallet
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)


class WalletDepositView(APIView):
    """
    API endpoint для пополнения баланса кошелька пользователя.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TransactionSerializer,
        responses={
            200: openapi.Response(
                description="Успешное пополнение баланса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER, example=150.00),
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="Сумма пополнения должна быть положительной"),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный запрос",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Учетные данные не были предоставлены."),
                    }
                )
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Пополнить баланс пользователя.

        Параметры запроса:
        - request (Request): Объект запроса, содержащий сумму пополнения.

        Возвращает:
        - Response: JSON-ответ с подтверждением пополнения и новым балансом
          пользователя или сообщение об ошибке валидации.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            request.user.wallet.deposit(amount)
            return Response({"status": "success", "balance": request.user.wallet.balance})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletWithdrawView(APIView):
    """
    API endpoint для списания средств с баланса кошелька пользователя.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TransactionSerializer,
        responses={
            200: openapi.Response(
                description="Успешное списание средств",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER, example=50.00),
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации или недостаточно средств",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="Недостаточно средств на счете"),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный запрос",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Учетные данные не были предоставлены."),
                    }
                )
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Списать средства с баланса пользователя.

        Параметры запроса:
        - request (Request): Объект запроса, содержащий сумму для списания.

        Возвращает:
        - Response: JSON-ответ с подтверждением списания и новым балансом
          пользователя или сообщение об ошибке в случае недостатка средств.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            try:
                request.user.wallet.withdraw(amount)
                return Response({"status": "success", "balance": request.user.wallet.balance})
            except ValueError as e:
                return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WalletRefundView(APIView):
    """
    API endpoint для возврата средств на баланс кошелька пользователя.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=TransactionSerializer,
        responses={
            200: openapi.Response(
                description="Успешный возврат средств",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="success"),
                        'balance': openapi.Schema(type=openapi.TYPE_NUMBER, example=150.00),
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example="error"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example="Сумма возврата должна быть положительной"),
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный запрос",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Учетные данные не были предоставлены."),
                    }
                )
            ),
        }
    )
    def post(self, request: Request) -> Response:
        """
        Вернуть средства на баланс пользователя.

        Параметры запроса:
        - request (Request): Объект запроса, содержащий сумму для возврата.

        Возвращает:
        - Response: JSON-ответ с подтверждением возврата и новым балансом
          пользователя или сообщение об ошибке валидации.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            request.user.wallet.refund(amount)
            return Response({"status": "success", "balance": request.user.wallet.balance})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBalanceView(LoginRequiredMixin, View):
    """
    Представление для отображения баланса кошелька пользователя на веб-странице.
    Пользователь должен быть аутентифицирован для доступа к этой странице.
    """

    template_name = 'wallet/balance.html'

    def get(self, request, *args, **kwargs):
        """
        Обработчик для GET запроса. Возвращает контекст с данными для страницы баланса.
        """
        # Создание контекста вручную
        context = {
            'username': request.user.username,
            'balance': request.user.wallet.balance,
            'balance_update_time': request.user.wallet.last_updated
        }
        return render(request, self.template_name, context)