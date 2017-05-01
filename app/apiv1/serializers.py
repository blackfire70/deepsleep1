from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework.validators import UniqueValidator


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=200,
        write_only=True,
        required=True
    )
    email = serializers.EmailField(
        max_length=30,
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    first_name = serializers.CharField(
        max_length=20,
        required=False,
        default=''
    )
    last_name = serializers.CharField(
        max_length=20,
        required=False,
        default=''
    )
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active')


class UserIncompleteSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'is_active',
            'is_staff',
            'last_login'
        )


class UserViewSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        read_only=True
    )
    password = serializers.CharField(
        max_length=200,
        write_only=True,
        required=True
    )
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'last_login'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=30,
        required=True
    )
    password = serializers.CharField(max_length=200, required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
