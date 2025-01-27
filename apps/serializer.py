from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField
from apps.models import User, Request


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


class RequestSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'user', 'reason', 'attachment', 'full_name', 'created_at', 'phone_number', 'is_read']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if not data.get("user"):
            raise ValidationError({"user": "User field is required."})
        if not data.get("reason"):
            raise ValidationError({"reason": "Reason field is required."})
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # user_id va username ni formatlash
        representation['user_id'] = instance.user.id if instance.user else None
        representation['username'] = instance.user.username if instance.user else "Unknown User"
        representation['user_info'] = instance.full_name
        representation['phone_number'] = instance.phone_number
        representation['created_at'] = instance.created_at.isoformat() if instance.created_at else None
        return representation
