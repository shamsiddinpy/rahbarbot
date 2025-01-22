from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField
from apps.models import User

class UserSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone', 'role', 'name', 'telegram_id', 'password', 'confirm_password')
        read_only_fields = ('telegram_id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        confirm_password = data.pop('confirm_password')
        if confirm_password != data.get('password'):
            raise ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user
