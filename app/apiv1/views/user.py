from django.contrib.auth.models import User

from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from apiv1.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
