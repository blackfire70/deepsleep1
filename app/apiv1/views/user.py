from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.validators import ValidationError
from django.utils import timezone

from oauthlib.common import generate_token
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import list_route
from oauth2_provider.models import AccessToken, Application
from oauth2_provider.ext.rest_framework import TokenHasScope
from apiv1.serializers import (
    UserViewSerializer,
    UserLoginSerializer,
    UserCreateSerializer,
)
from core.utils.mail import send_activation_mail


def create_token(user):
    '''
    Creates an AccessToken object for the user and application 'myapp'
    :param user: User instance
    :param type: class
    '''
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
    serializer_class = UserViewSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    @list_route(method=['post'])
    def change_password(self, request):
        '''
        Resource:
        api/v1/user/change-password
        '''
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(request.data['password'])
            user.save()
            return Response({'message':'password changed.'}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserCreateViewSet(viewsets.ModelViewSet):

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    def create(self, request):
        '''
        Resource:
        api/v1/user/signup
        
        Creates inactive user instance and sends an activation email to the user.
        '''
        
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
                token = create_token(user)
                #TO DO: convert mail sending to a celery task
                send_activation_mail(user=user)
                return Response(
                    self.get_serializer(user).data,
                    status=status.HTTP_201_CREATED
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def activate(self, request, pk=None):
        '''
        Resource:
        api/v1/user/activate/<pk>/
        
        Sets the user's is_active = True after validation of the token
        '''
        user = User.objects.get(id=pk)
        token = request.GET['token']
        token = token.replace(' ', '+')
        algo, salt, p_hash = user.password.split('$', 2)
        if token == p_hash:
            user.is_active = True
            user.save()
            return Response({'message': 'account activated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'invalid token'}, status=status.HTTP_401_UNAUTHORIZED)



class UserLoginViewSet(viewsets.ModelViewSet):

    serializer_class = UserLoginSerializer
    queryset = User.objects.all()
    @list_route(methods=['post'])
    def login(self, request):
        '''
        Resource:
        api/v1/user/activate/login/
        
        User login. After authentication, the user is logged in and a bearer token is given.
        '''
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
