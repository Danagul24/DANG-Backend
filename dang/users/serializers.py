from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=90)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)
    is_seller = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'is_seller']

    def validate(self, attr):
        email_exists = User.objects.filter(email=attr['email']).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attr)

    # hash password
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)

        user.set_password(password)
        user.save()

        return user

