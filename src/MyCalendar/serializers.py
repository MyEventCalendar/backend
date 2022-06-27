from urllib import request

from .models import Event, User
from rest_framework import serializers
from django.contrib.auth import authenticate


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['pk', 'name', 'description', 'start_time', 'end_time', 'hidden', 'user']

    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.hidden = validated_data.get('hidden', instance.hidden)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['telegram_id', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        telegram_id = data.get('telegram_id', None)
        password = data.get('password', None)
        if telegram_id is None:
            raise serializers.ValidationError(
                'An id is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=telegram_id, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this id and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )
        return {
            'telegram_id': user.telegram_id,
            'username': user.username
        }
