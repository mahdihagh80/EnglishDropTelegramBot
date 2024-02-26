from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, Package, BankAccount, TelegramUser
from rest_framework.generics import (
    get_object_or_404,
    CreateAPIView,
    RetrieveUpdateAPIView,
    ListAPIView,
    UpdateAPIView
)

from .serializers import (
    PackageSerializer,
    TransactionSerializer,
    TelegramUserSerializer,
    BankAccountSerializer
)


class TelegramUserCreateView(CreateAPIView):
    serializer_class = TelegramUserSerializer


class TransactionUpdateView(UpdateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
  

class TransactionCreate(CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class BankAccountRetrieveView(APIView):
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.filter(active=True)

    def get(self, request):
        instance = self.queryset[0]
        serializer = self.serializer_class(instance)
        return Response(serializer.data)


class PackageView(APIView):
    serializer_class = PackageSerializer
    queryset = Package.objects.filter(active=True)

    def get(self, request, pk=None):
        if pk:
            instance = get_object_or_404(self.queryset, pk=pk)
        else:
            instance = self.queryset[0]
            
        serializer = self.serializer_class(instance)
        return Response(serializer.data)