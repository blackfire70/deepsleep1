from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import viewsets, status
from apiv1.serializers import UserSerializer
from rest_framework.response import Response
from django.core.validators import ValidationError

class CreateUserView(CreateAPIView):

    model = User
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = User(
                first_name=serializer.data.get('first_name') or '',
                last_name=serializer.data.get('last_name') or '',
                email=serializer.data['email'],
                username=serializer.data['email'],
                is_active=False
            )

            user.set_password(serializer.data['password'])
            try:
                user.full_clean()
            except ValidationError as e:
                return Response(
                    {'error':'cause:{}'.format(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user.save()
                return Response(
                    self.get_serializer(user),
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


