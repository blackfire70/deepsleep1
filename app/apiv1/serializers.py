from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import ValidationError
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=200, write_only=True, required=True)
    email = serializers.EmailField(
        max_length=30,
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
        )
    first_name = serializers.CharField(max_length=20, required=False, default='')
    last_name = serializers.CharField(max_length=20, required=False, default='')
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_data):

        user = get_user_model()(
            first_name=validated_data.get('first_name') or '',
            last_name=validated_data.get('last_name') or '',
            email=validated_data['email'],
            username=validated_data['email'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()

        class Meta:
            model = get_user_model()
            fields = ('email', 'password', 'first_name', 'last_name')
