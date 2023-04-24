from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Wallet
from .schemas import RequestKinds
from .serializers import WalletSerializer, CreateRequestSerializer
from .services import create_request


class CreateWalletView(CreateAPIView):
    serializer_class = WalletSerializer


class RetrieveWalletView(RetrieveAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    lookup_field = "uuid"


class CreateDepositView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            create_request(request.user, RequestKinds.Deposit, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleWithdrawView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateRequestSerializer(data=request.data)
        if serializer.is_valid():
            create_request(request.user, RequestKinds.Withdraw, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
