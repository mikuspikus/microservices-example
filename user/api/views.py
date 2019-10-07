from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView, Request, Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from api.serializers import CustomUserSerializer
from api.models import CustomUser

# Create your views here.
class UserInfoView(APIView):

    permission_classes = (IsAuthenticated, )

    def get(self, request: Request, *args, **kwargs) -> Response:
        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(instance = request.user)

        return Response(data = serializer.data, status = status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(instance = request.user, data = request.data)
        
        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.data, status = status.HTTP_202_ACCEPTED)

        return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        if request.user is None:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        request.user.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)


class UsersView(ListCreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return CustomUser.objects.all()


class UserView(APIView):
    permissions_classes = (IsAuthenticated, )

    def get(self, request: Request, user_id: int) -> Response:
        try:
            user_ = CustomUser.objects.get(id = user_id)

        except CustomUser.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(instance = user_)

        return Response(data = serializer.data, status = status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request : Request, *args, **kwargs) -> Response:
        serializer = CustomUserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(data = serializer.errors, status = status.HTTP_400_BAD_REQUEST)