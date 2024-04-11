from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import UserProfile

User = get_user_model()


class CreateProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = 'address1', 'address2', 'city', 'state', 'zip_code'

    def clean_zip_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('The ZIP code shouldn\'n contain letters')
        return value


class CreateUserSerializer(serializers.ModelSerializer):
    profile = CreateProfileSerialzer()

    # TODO: make first name and last name as required in the User model
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = 'email', 'password', 'first_name', 'last_name', 'profile'

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user, **profile_data)
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists")
        return value
