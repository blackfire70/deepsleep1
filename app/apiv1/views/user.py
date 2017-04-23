from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.validators import ValidationError
from django.utils import timezone

from oauthlib.common import generate_token
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from oauth2_provider.models import AccessToken, Application

from apiv1.serializers import UserSerializer, UserLoginSerializer


def create_token(user):
    expire_second = settings.OAUTH2_PROVIDER['ACCESS_TOKEN_EXPIRE_SECONDS']
    expires = timezone.now() + timezone.timedelta(seconds=expire_second)
    scopes = settings.OAUTH2_PROVIDER['SCOPES']
    app = Application.objects.get(name='myapp')
    access_token = AccessToken.objects.create(
        user=user,
        application=app,
        expires=expires,
        scope=scopes,
        token=generate_token()
    )
    return access_token

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

            user.set_password(request.data['password'])
            try:
                user.full_clean()
            except ValidationError as e:
                return Response(
                    {'error':'cause:{}'.format(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                user.save()
                create_token(user)
                return Response(
                    self.get_serializer(user).data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserLoginViewSet(viewsets.ModelViewSet):

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    @list_route(methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data['email'],
                password=request.data['password']
            )
            if user and user.is_active==True:
                login(request, user)
                token = AccessToken.objects.get(user=user).token
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'message': 'Invalid email/password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )